from src.infrastructure.tender_finder import PageTendersParser


def test_get_xml_utl_by_number():
    url = 'https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=1234567'
    assert PageTendersParser().get_xml_url_by_number('1234567') == url
