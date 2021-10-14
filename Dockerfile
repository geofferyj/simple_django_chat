FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PRODUCTION True
ENV DJANGO_SETTINGS_MODULE core.settings
ENV REDIS_HOST redis
RUN apk update && \
    apk add --virtual build-deps libffi-dev curl openssl-dev gcc python3-dev musl-dev && \
    apk add bash 

RUN mkdir /config
ADD requirements.txt /config/
RUN curl https://bootstrap.pypa.io/get-pip.py | python
RUN pip install --upgrade setuptools
RUN pip install -r /config/requirements.txt
RUN mkdir /src
ADD . /src/
WORKDIR /src
RUN python manage.py migrate

EXPOSE 8000
CMD [ "python", "manage.py", "runserver","0.0.0.0:8000"]