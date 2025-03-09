import time

from src.infrastructure.celery.app import celery_app
from src.service.tasks import register_tasks

register_tasks(celery_app=celery_app)


def send_task_with_timeout(url: str):
    task = celery_app.send_task(
        name='find_publish_date',
        args=(url, None,),
    )
    time.sleep(0.5)
    return task


def main():
    print('Старт парсинга')
    task1 = celery_app.send_task(
        name='find_url_xml',
        args=(1,)
    )
    time.sleep(2)
    task2 = celery_app.send_task(
        name='find_url_xml',
        args=(2,),

    )
    print('Задачи на каждую из страниц созданы')

    result1 = task1.get()
    while not task2.ready():
        time.sleep(0.5)
    result2 = task2.get()

    links = result1['links'] + result2['links']
    print('len links:', len(links))
    xml_task_ids = list(map(
        send_task_with_timeout,
        links
    ))
    print('id Задач на парсинг xml', xml_task_ids)
    while xml_task_ids:
        for task in xml_task_ids[:]:
            if task.ready():  # Проверяем, завершилась ли задача
                try:
                    print(f"Результат: {task.get()}")
                    xml_task_ids.remove(task)
                except Exception as e:  # noqa
                    pass
        if xml_task_ids:
            print("Ожидание завершения оставшихся задач...")
            time.sleep(10)  # Подождём немного перед следующей проверкой

    print("Все задачи завершены.")
