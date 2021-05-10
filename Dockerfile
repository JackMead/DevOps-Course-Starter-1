FROM python:3 as base

WORKDIR /data
COPY ./poetry.toml /data
COPY ./pyproject.toml /data
RUN pip install poetry && poetry install

FROM base as production
RUN apt-get update && \
    apt-get install -y gunicorn
COPY ./todo_app /data/todo_app
EXPOSE 5000
ENTRYPOINT $(poetry env info --path)/bin/gunicorn --error-logfile /data/error.log -b 0.0.0.0:5000 "todo_app.app:create_app()"

FROM base as development
EXPOSE 5000
ENTRYPOINT  poetry run flask run --host 0.0.0.0

