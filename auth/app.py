from fastapi import FastAPI

from auth.app_factory import get_app

app: FastAPI = get_app()