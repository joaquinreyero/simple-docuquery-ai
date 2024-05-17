from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import sentry_sdk

import os

from src.models.models import Base


class Settings:
    def __init__(self):
        if os.getenv("ENV") == "local":
            self.DATABASE_URI = os.getenv("DATABASE_URI_LOCAL")
        else:
            self.DATABASE_URI = os.getenv("DATABASE_URI")
        self.DSN_SENTRY = os.getenv("DSN_SENTRY")


def configure_app(app: FastAPI):
    configure_cors(app)
    configure_sentry(app)


def configure_cors(app: FastAPI):
    origins = [
        "*",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_sentry(app: FastAPI):
    sentry_sdk.init(
        dsn=Settings().DSN_SENTRY,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    app.add_middleware(SentryAsgiMiddleware)


def configure_database():
    engine = create_engine(Settings().DATABASE_URI)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return session_local()


settings = Settings()