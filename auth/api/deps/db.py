# Dependency
from typing import Generator, Optional

from fastapi import Depends
from sqlalchemy.engine import Engine as Database
from sqlalchemy.orm import Session
from starlette.requests import Request

from auth.db.connection import get_db_conn_DO_NOT_USE


def get_db(
    request: Request, db_conn: Optional[Database] = Depends(get_db_conn_DO_NOT_USE)
) -> Generator[Session, None, None]:
    db_session = Session(
        autocommit=False, autoflush=False, bind=db_conn, expire_on_commit=False
    )
    request.state.db_session = db_session

    try:
        yield db_session
    finally:
        db_session.close()