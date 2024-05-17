from fastapi import status, APIRouter

from sqlalchemy.orm import Session

from contextlib import contextmanager

from src import config
from src.models import models

router = APIRouter(
    prefix="/api",
    tags=['Health Check']
)


@router.get("/hello-world", status_code=status.HTTP_200_OK)
async def hello_world():
    """
    Test the health of the service.
    """
    return {"message": "Hello World!"}



@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Verify the health of services.
    """

    class UserRepository:
        @staticmethod
        @contextmanager
        def get_db() -> Session:
            db = config.SessionLocal()
            try:
                yield db
            finally:
                db.close()

    def test():
        with UserRepository.get_db() as db:
            try:
                db.query(models.Test).first()
                return {"status": "ok", "message": "Database connection is healthy"}
            except Exception as e:
                return e

    return test()


@router.get("/sentry-debug", status_code=status.HTTP_200_OK)
async def trigger_error():
    """
    Verify the Sentry error tracking.
    """
    division_by_zero = 1 / 0