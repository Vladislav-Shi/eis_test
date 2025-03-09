from src.service.tasks.url_parce import UrlFinderTask
from src.service.tasks.xml_parce import XmlParseTask


def register_tasks(celery_app):
    celery_app.register_task(XmlParseTask())
    celery_app.register_task(UrlFinderTask())
