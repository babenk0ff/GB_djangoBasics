FROM python:3.9.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/app
RUN addgroup -S app && adduser -S app -G app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
#RUN mkdir $APP_HOME/static
RUN mkdir -p $APP_HOME/var/log/
RUN mkdir -p $APP_HOME/var/emails-tmp/
WORKDIR $APP_HOME

RUN apk update && \
    apk add gcc musl-dev linux-headers python3-dev postgresql-dev

RUN pip install --upgrade pip
COPY ../../requirements.txt .
RUN pip install -r requirements.txt

COPY ../../ $APP_HOME

RUN chown -R app:app $APP_HOME

USER app