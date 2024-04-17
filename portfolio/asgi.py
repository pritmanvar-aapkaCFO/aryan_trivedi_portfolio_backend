import os
from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
apps.populate(settings.INSTALLED_APPS)

from contact.routes import contact_router
from myimages.routes import image_router

def get_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
    SECRET_KEY = "wqwq"
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(contact_router, tags=["contact"], prefix="/api/contact")
    app.include_router(image_router, tags=["contact"], prefix="/api/images")
    app.mount("/", WSGIMiddleware(get_wsgi_application()))

    return app


app = get_application()
