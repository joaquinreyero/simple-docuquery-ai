from fastapi import FastAPI

from src.api import health
from src.config import configure_cors, configure_sentry

app = FastAPI()

configure_cors(app)
configure_sentry(app)

app.include_router(health.router)