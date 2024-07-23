"""
The usual way of using SQLAlchemy thread-local scoped sessions
doesn't mix well with FastAPI since a single thread could handle
multiple requests. Request A could close the Session while
Request B is in the middle of using it.

In order to account for this, we implement Session management
at a request level instead of at the thread level.

See: https://github.com/tiangolo/fastapi/issues/726
"""

from sqlalchemy.engine import Engine as Database

# pylint: disable=W0603, C0103
_db_conn: Database


def set_db_conn(db_conn: Database) -> None:
    global _db_conn
    _db_conn = db_conn


def close_db_conn() -> None:
    global _db_conn
    if _db_conn:
        _db_conn.dispose()

def get_db_conn_DO_NOT_USE() -> Database:
    """
    Do not use this directly in API endpoints.
    Use get_db from db.py instead
    """
    return _db_conn