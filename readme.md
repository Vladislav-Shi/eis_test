Запуск
1) Устанвоить библиотеки
    ```commandline
    poetry install  # если используется пооетри
   ```
    ```commandline
    pip install poetry
    poetry install
    ```

2) Создать `.env` в корне и заполнить на основе `.env.template`
3) `python run.py` для запуска 

##### Проблемы возникшие при выполнении ТЗ:
- У сайте имеется жесткий rate limit по запросом. Лучше использовать несколько прокси
