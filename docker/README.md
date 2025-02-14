# djfapi-btceth
Example using Django application inside your FastAPI application, to get (store and show) the latest block for BTC and ETH

For development using docker-compose
====================================

1. Створити .env (якщо ще немає)
Створи файл .env у корені проєкту та додай змінні середовища:
POSTGRES_DB=mydatabase
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_HOST=db
POSTGRES_PORT=5477

2. Запустити docker-compose

    chmod +x docker/entrypoint.sh
    cd docker
    docker compose -f docker-compose.local.yml up --build

Що працює після запуску?
------------------------

Nginx (Frontend)	http://localhost:88/
Django	http://localhost:8888
FastAPI	http://localhost:8888/api/hello
Admin панель	http://localhost:8888/admin/
RabbitMQ	http://localhost:15677
PostgreSQL	localhost:5477
Redis	localhost:6377

Celery	Фонові завдання

Дивитися логи

    docker-compose logs django | tail -n 50

Перезапустити контейнер
=======================

    docker-compose down
    docker-compose build django
    docker-compose up -d
