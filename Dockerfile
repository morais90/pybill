# build stage
FROM python:3-alpine as builder

RUN mkdir /install \
&& apk add --no-cache \
  gcc \
  musl-dev \
  postgresql-dev \
  zlib-dev \
  jpeg-dev \
  libxml2-dev \
  libxslt-dev

ADD . /code
WORKDIR /code

RUN pip install --upgrade pip

# development stage
FROM builder as development

RUN apk add --no-cache postgresql-client \
&& pip install --no-cache-dir --requirement requirements/development.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0:8000"]

# production stage
FROM builder as production

RUN pip install --no-cache-dir --requirement requirements/production.txt

EXPOSE 80
CMD ["gunicorn", "monitorweb.wsgi", "--bind=0.0.0.0:80", "--workers=4"]