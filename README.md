# short-url

## Description

- Turn web url into 5 words.
- Expire short url after 300 seconds. Re-counting the time if anyone connect to the short url before it expired.
- List all availables short urls.

## Pre-Conditions

- [Docker](https://docs.docker.com/get-docker/) is installed
- [docker-compose](https://docs.docker.com/compose/install/#install-compose) is installed

## How to start

- Configure environment variables

```shell
mv .env.example .env
```

- Start service:

```shell
sh manage.sh start_service
```

- Visit `http://127.0.0.1:5000/short-url/home`

- Stop service:

```shell
sh manage.sh stop_service
```

## How to test

- Run tests (container)
  - Execute test command

  ```shell
  sh manage.sh test
  ```

- Run tests (local)
  - Ensure `redis` is set
  - Configure `.env_test` && `TestSettings` in `settings.py`
  - Set environment variable

  ```shell
  export FLASK_ENV=test
  ```

  - Execute test command

  ```shell
  pytest --cov
  ```
