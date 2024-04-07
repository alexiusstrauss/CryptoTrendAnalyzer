FROM python:3.10-slim-buster

WORKDIR /app
ENV APP_NAME=cryptotrendanalyzer-api
ARG DEV_MODE=true
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TZ America/Sao_Paulo
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH $PROJECT_DIR/app:$PYTHONPATH

RUN apt-get update -yy  \
    && apt-get upgrade -yy \
    && apt-get install -yy libpq-dev git cron \
    && pip install --upgrade pip \
    && pip install --no-cache-dir pipenv

COPY Pipfile* .

RUN bash -c "if [ $DEV_MODE == 'true' ] ; \
    then pipenv install --dev ; else pipenv install; fi"

COPY ./app/ /app/

EXPOSE 8000

CMD [ "python", "manage.py", "runserver",  "0.0.0.0:8000"]
