# djfapi-btceth
Example using Django application inside your FastAPI application, to get (store and show) the latest block for BTC and ETH


For development
================

Enter the project folder and create a virtual environment for python, execute:

    python3 -m venv .venv3

then activate the virtual environment:

    . .venv3/bin/activate

Install all packages and make migrations:

    pip install pip wheel -U
    make local


Project Folder Structure
========================

repo_root/                     # Project root directory
│── docker/                    # Docker-related files
│   ├── django.Dockerfile      # Dockerfile for Django (ASGI + Uvicorn)
│   ├── celery.Dockerfile      # Dockerfile for Celery worker
│   ├── nginx.Dockerfile       # Dockerfile for Nginx reverse proxy
│   ├── entrypoint.sh          # Entry script for container initialization
│   ├── nginx.conf             # Nginx configuration file
│── requirements/              # Dependency management
│   ├── base.pip               # Base dependencies
│   ├── local.pip              # Local development dependencies
│   ├── code-checks.pip        # Linters and code formatting dependencies
│── src/                       # Main source code directory
│   ├── djapps/                # Django applications
│   │   ├── app1/              # Example Django app
│   │   ├── app2/              # Another Django app
│   ├── faproject/             # FastAPI application
│   ├── project/               # Django project configuration (settings, URLs, etc.)
│── allstatic/                 # Collected static files
│── media/                     # Uploaded media files
│── .env                       # Environment variables (not committed to VCS)
│── docker-compose.local.yml   # Docker Compose file for local development
