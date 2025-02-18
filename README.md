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
│── allstatic/                 # Collected static files
│── media/                     # Uploaded media files
│── docker/                    # Docker-related files
│   ├── localdev/server.Dockerfile      # Dockerfile for Django (ASGI + Uvicorn) and Celery worker with Beat
│   ├── localdev/nginx.Dockerfile       # Dockerfile for Nginx reverse proxy
│   ├── localdev/nginx.conf             # Nginx configuration file
│   │── .env                       # Environment variables (not committed to VCS)
│   │── docker-compose.local.yml   # Docker Compose file for local development
│   ├── entrypoint.sh          # Entry script for container initialization
│── requirements/              # Dependency management
│   ├── base.pip               # Base dependencies
│   ├── code-checks.pip        # Linters and code formatting dependencies
│   ├── local.pip              # Local development dependencies
│── src/                       # Main source code directory
│   ├── djapps/                # All our Django applications
│   │   ├── bstore/                 # bstore app
│   ├── djproject/             # Django project configuration (settings, URLs, etc.)
│   ├── faproject/             # FastAPI application
│   ├── manage.py
│── .gitignore
│── Makefile
│── README.md