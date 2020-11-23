#!/bin/sh

ACTION=$1

case $ACTION in
"start_service")
  docker-compose --env-file .env up -d --build
  ;;
"stop_service")
  docker-compose down
  ;;
"test")
  docker-compose up --no-start --build && \
    ENV_FILE=.env_test docker-compose --env-file .env_test run app pytest --cov

  docker-compose down
  ;;
*)
  echo "ACTION not in [start_service, stop_service, test]"
  ;;
esac
