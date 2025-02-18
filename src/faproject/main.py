import os

import django
from django.conf import settings
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djproject.settings")
django.setup()

from .api import router as api_router

# Create FastAPI app
app = FastAPI(
    title="BStore API",
    description="API for BTC and ETH blocks",
    version="0.1.0",
)
# Get Django ASGI application
django_app = get_asgi_application()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production we need replace with allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def api_root():
    return {"Hello": "FastAPI"}


# Include API routes
app.include_router(
    api_router,
    prefix="/api",
    tags=["blocks"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(settings.STATIC_ROOT)), name="static")

# Mount media files
app.mount("/media", StaticFiles(directory=str(settings.MEDIA_ROOT)), name="media")

app.mount("/", django_app)
