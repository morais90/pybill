# Olist Calls

[![CircleCI](https://circleci.com/gh/morais90/work-at-olist/tree/master.svg?style=svg)](https://circleci.com/gh/morais90/work-at-olist/tree/master) [![Heroku](https://heroku-badge.herokuapp.com/?app=work-at-olist-calls)]


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
