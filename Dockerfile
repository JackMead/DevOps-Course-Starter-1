FROM python:3.10.0a7-buster as base

WORKDIR /todo_app
RUN pip install poetry gunicorn flask
COPY /todo_app /data/todo_app

EXPOSE 5000

FROM base as production
WORKDIR /data
ENV PYTHONPATH /data/todo_app
ENTRYPOINT ["/usr/local/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "-t", "30", "todo_app.app:create_app()"]

