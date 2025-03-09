### Запуск
1) Устанвоить библиотеки
    ```commandline
    poetry install  # если используется пооетри
   ```
    ```commandline
    pip install poetry
    poetry install
    ```

2) Создать `.env` в корне и заполнить на основе `.env.template`
3) `celery -A src.main.celery_app worker --loglevel=info` для запуска воркеров
4) `python run.py` для запуска спкрипта обхода 2 страниц

### Проблемы возникшие при выполнении ТЗ:
- У сайте имеется жесткий rate limit по запросом. Лучше использовать несколько прокси или повторять задачу через некоторое время
