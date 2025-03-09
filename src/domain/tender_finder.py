from abc import ABC, abstractmethod
from typing import List

from src.domain.models import Fz44Tender


class AbstractPageTendersParser(ABC):

    @abstractmethod
    def find_tenders_page(self, page_num: int) -> str:
        pass

    @abstractmethod
    def get_xml_by_url(self, url: str) -> str:
        pass

    @abstractmethod
    def get_xml_by_number(self, number: str) -> str:
        pass

    @abstractmethod
    def get_xml_url_by_number(self, number: str) -> str:
        pass


class AbstractTenderParser(ABC):

    @abstractmethod
    def find_tender_numbers_by_page(self, html: str) -> List[str]:
        pass

    @abstractmethod
    def get_info_by_xml(self, xml: str) -> Fz44Tender:
        pass
