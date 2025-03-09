FROM python:3.12-alpine
RUN apk add --no-cache gcc musl-dev libffi-dev

COPY . /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE false

RUN pip config set global.trusted-host 212.193.30.165:9090
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction

ENTRYPOINT ["python"]
CMD ["run.py"]