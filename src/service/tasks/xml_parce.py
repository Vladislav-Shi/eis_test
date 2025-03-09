import logging

import celery

from src.infrastructure.tender_finder import PageTendersParser, TenderParser
from src.service.tender_finder import get_fz_publish_date


class XmlParseTask(celery.Task):
    name = 'find_publish_date'
    max_retries = 10
    default_retry_delay = 60
    rate_limit = '2/s'

    def run(self, url: str, proxy: str | None = None):
        try:
            logging.info(f'start XmlParseTask with {url=}')
            tender_page_parser = PageTendersParser(proxy=proxy)
            tender_parser = TenderParser()
            res = get_fz_publish_date(
                url=url,
                tender_page_finder=tender_page_parser,
                tender_finder=tender_parser,
            )
            res = res.dict()
            res.update({'key': 'find_publish_date'})
            return res
        except Exception as e:
            logging.error(e)
            raise self.retry(exc=e, countdown=self.default_retry_delay)
