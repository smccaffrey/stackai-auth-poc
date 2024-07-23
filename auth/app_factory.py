import platform
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine

from auth import settings
from auth.api import routes
from auth.db.connection import set_db_conn, close_db_conn


__RECOMMENDED_PYTHON_VERSION__: str = "^3.11"

APM_SERVICE_NAME: str = "AUTH"

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    """Instantiate a auth FastAPI instance. This instance will
    be parametrized by the values in auth.settings.
    """
    app = FastAPI()  # type: ignore

    def open_database_connection_pools() -> None:
        engine = create_engine(
            settings.DATABASE_URL, pool_size=32, max_overflow=64, pool_pre_ping=True  # type: ignore
        )
        set_db_conn(engine)

    def close_database_connection_pools() -> None:
        close_db_conn()

    app.on_event("startup")(open_database_connection_pools)
    app.on_event("shutdown")(close_database_connection_pools)

    logger.info("Initializing auth service")

    if platform.python_version() != __RECOMMENDED_PYTHON_VERSION__:
        logger.warning(
            f"Running on Python {platform.python_version()}. "
            f"The recommended Python is {__RECOMMENDED_PYTHON_VERSION__}."
        )

    app.include_router(router=routes.root_router)

    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
    )

    return app