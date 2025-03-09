from datetime import datetime, timedelta, timezone

from src.domain.models import Fz44Tender
from src.infrastructure.settings import BASE_DIR
from src.infrastructure.tender_finder import TenderParser


def test_find_numbers_in_page():
    result_data = ['0188300004525000013',
                   '0700500004225000011',
                   '0316300000125000004',
                   '0316300000125000003',
                   '0352300059325000087',
                   '0352300059325000088',
                   '0322200017925000006',
                   '0352300059325000086',
                   '0362300156925000003',
                   '0151300050825000005']
    with open(BASE_DIR / 'tests' / 'data' / 'page_with_tender.html') as file:
        html = file.read()
    result = TenderParser().find_tender_numbers_by_page(html)
    assert result == result_data


def test_find_numbers_in_wrong_page():
    html = '''<body>ERROR PAGE</body>'''
    result = TenderParser().find_tender_numbers_by_page(html)
    assert result == []


def test_xml_parce():
    result = Fz44Tender(
        number='0188300004525000013',
        publish_in_eis=datetime(2025, 3, 8, 22, 9, 40, 253000, tzinfo=timezone(timedelta(seconds=43200)))
    )
    with open(BASE_DIR / 'tests' / 'data' / 'viewXml.html.xml') as file:
        xml_file = file.read()
    result2 = TenderParser().get_info_by_xml(xml_file)
    assert result.publish_in_eis == result2.publish_in_eis
    assert result.number == result2.number
