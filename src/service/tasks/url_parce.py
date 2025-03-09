import logging

import celery

from src.infrastructure.tender_finder import PageTendersParser, TenderParser
from src.service.tender_finder import get_tenders_xml_url_by_page


class UrlFinderTask(celery.Task):
    name = 'find_url_xml'
    rate_limit = 10
    default_retry_delay = 30
    max_retries = 10

    def run(self, page: int, proxy: str | None = None):
        try:
            logging.info(f'start UrlFinderTask with {page=}')
            tender_page_parser = PageTendersParser(proxy=proxy)
            tender_parser = TenderParser()
            res = get_tenders_xml_url_by_page(
                page=page,
                tender_page_finder=tender_page_parser,
                tender_finder=tender_parser,
            )
            return {'links': res, 'key': 'find_url_xml'}
        except Exception as e:
            logging.error(e)
            raise self.retry(exc=e, countdown=self.default_retry_delay)
