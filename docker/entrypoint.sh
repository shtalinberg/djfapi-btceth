#!/bin/sh

echo "Зачекайте, поки база даних стане доступною..."
while ! nc -z pg 5432; do
  sleep 1
done
echo "База даних доступна!"

if ! python manage.py migrate; then
  echo "Error: Migrations failed. Exiting."
  exit 1
fi

if ! python manage.py collectstatic --noinput; then
  echo "Error: Static collection failed. Exiting."
  exit 1
fi

echo "Starting Uvicorn..."

# Не запускаємо сервер, оскільки це зробить docker-compose
exec "$@"
