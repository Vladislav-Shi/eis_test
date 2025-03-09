import re
from datetime import datetime
from typing import List

import requests
import xmltodict
from bs4 import BeautifulSoup, Tag

from src.domain.models import Fz44Tender
from src.domain.tender_finder import (AbstractPageTendersParser,
                                      AbstractTenderParser)
from src.exeptions import NotFoundError, ValidationError


class PageTendersParser(AbstractPageTendersParser):

    def __init__(self, proxy: str | None = None):
        self.proxy = proxy

    def find_tenders_page(self, page_num: int) -> str:
        if page_num < 1:
            raise ValidationError('страница должна быть больше 1')
        result = requests.get(
            f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber={page_num}',
            proxies=self.proxy
        )

        if result.status_code != 200:
            raise NotFoundError(f'Ошибка получения тела ответа {result.status_code=} {page_num=}')
        html_body = result.text
        return html_body

    def get_xml_by_number(self, number: str) -> str:
        result = requests.get(
            self.get_xml_url_by_number(number),
            proxies=self.proxy
        )
        if result.status_code != 200:
            raise NotFoundError('Ошибка получения тела ответа')
        xml_body = result.text
        return xml_body

    def get_xml_by_url(self, url: str) -> str:
        result = requests.get(url, proxies=self.proxy)
        if result.status_code != 200:
            raise NotFoundError(f'Ошибка получения тела ответа {result.status_code=} {url=}')
        xml_body = result.text
        return xml_body

    def get_xml_url_by_number(self, number: str) -> str:
        return f'https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber={number}'


class TenderParser(AbstractTenderParser):
    @staticmethod
    def _get_number_by_div(el: Tag) -> str:
        return re.findall(r'\d+', el.find('a').text)[0]

    def find_tender_numbers_by_page(self, html: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find_all('div', class_='registry-entry__header-mid__number')
        return [self._get_number_by_div(el) for el in elements]

    def get_info_by_xml(self, xml: str) -> Fz44Tender:
        xml_content = xmltodict.parse(xml)
        xml_content = list(xml_content.values())[0]
        publish_date = xml_content['commonInfo'].get('publishDTInEIS')

        if publish_date:
            publish_date = datetime.fromisoformat(publish_date)
        return Fz44Tender(
            number=xml_content['commonInfo'].get('purchaseNumber'),
            publish_in_eis=publish_date,
        )
