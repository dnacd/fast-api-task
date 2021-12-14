#!/bin/sh

if [ "$MYSQL_DATABASE" = "postgres" ]
then
    echo "Waiting for Postgres..."
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.5
    done
    echo "MariaDB started"
fi
exec "$@"