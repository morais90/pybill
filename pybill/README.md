## PyBill

[![CircleCI](https://circleci.com/gh/morais90/pybill/tree/master.svg?style=svg)](https://circleci.com/gh/morais90/pybill/tree/master)
PyBill is an application that helps in tracking the calls that your company makes. Through it, it's possible to monitor and audit in real time all the data necessary for good management. The relevant data reports allow you to take care of your business in a much simpler way.

## Set up the Docker environment

### Installing dependencies
- Install [docker-compose](https://docs.docker.com/compose/install)

### Initialize the containers
```
shell
# docker-compose up
```
At this time the aplication will be available in http://127.0.0.1:8000

### Apply initial migrations
```
shell
# docker-compose exec pybill python manage.py migrate
```

### Run tests
```
shell
# docker-compose exec pybill python manage.py test --verbosity 2 --noinput --settings pybill.core.settings_test tests
```

### Run linter
```
shell
# docker-compose exec pybill pycodestyle pybill/
```

### API Documentation

The API documentation access is allowed through the URL `/docs/` path. The documentation explain the available methods and the parameters for each context.

### Browse the API

It's able to browse the API endpoints with the browsable API. To access the browsable API you only need to use the endpoint at a browser environment.

### Continous Integration

All commands to provisioning infrastructure are in Heroku manifest file (heroku.yml), this file would be in root directory of this application. The heroku.yml file specifies the docker images build and configurations for the application provisioning.

### Environment variables

Some predefined variables are necessary by this service. This variables are used on CircleCI and Heroku.

| Variable      | Description                   | Format                                    |
|---------------|-------------------------------|-------------------------------------------|
| DATABASE_URL  | Django database URL           | engine://user:password@host:port/database |
| DEBUG         | Django debug flag             | true|false                                |
| ALLOWED_HOSTS | Django allowed hosts          | host1,host2,host3                         |
| SECRET_KEY    | Django application secret key | hash                                      |
| SENTRY_DSN    | Sentry DSN                    | https://XXXX@sentry.io/XXXX               |
