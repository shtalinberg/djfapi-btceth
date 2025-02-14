import os

import django
from django.conf import settings
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djproject.settings")
django.setup()

# Create FastAPI app
app = FastAPI()
# Get Django ASGI application
django_app = get_asgi_application()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.mount("/", django_app)

# Mount static files
app.mount("/static", StaticFiles(directory=str(settings.STATIC_ROOT)), name="static")

# Mount media files
app.mount("/media", StaticFiles(directory=str(settings.MEDIA_ROOT)), name="media")


