# build stage
FROM python:3-alpine as builder

ENV PYTHONUNBUFFERED=1

RUN mkdir /install \
&& apk add --no-cache \
  gcc \
  musl-dev \
  postgresql-dev \
  zlib-dev \
  jpeg-dev \
  libxml2-dev \
  libxslt-dev \
  curl

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

CMD ["gunicorn", "olist.core.wsgi", "--bind=0.0.0.0:80", "--workers=4"]