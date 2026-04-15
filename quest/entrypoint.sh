#!/bin/sh

# Ждем пока запустится PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Делаем миграции
python manage.py migrate

# Запускаем сервер
python manage.py runserver 0.0.0.0:8000