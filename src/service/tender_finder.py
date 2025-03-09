from src.domain.models import Fz44tenderWithUrl
from src.domain.tender_finder import (AbstractPageTendersParser,
                                      AbstractTenderParser)


def get_tenders_xml_url_by_page(
        tender_page_finder: AbstractPageTendersParser,
        tender_finder: AbstractTenderParser,
        page: int,
) -> list[str]:
    html_page = tender_page_finder.find_tenders_page(page_num=page)
    res = tender_finder.find_tender_numbers_by_page(
        html=html_page
    )
    return [tender_page_finder.get_xml_url_by_number(i) for i in res]


def get_fz_publish_date(
        tender_page_finder: AbstractPageTendersParser,
        tender_finder: AbstractTenderParser,
        url: str
):
    xml_page = tender_page_finder.get_xml_by_url(url)
    try:
        res = tender_finder.get_info_by_xml(
            xml=xml_page
        )
    except KeyError as e:
        raise ValueError(f'key error in {url=} {e=}')
    return Fz44tenderWithUrl(
        publish_in_eis=res.publish_in_eis,
        number=res.number,
        xml_url=url
    )
