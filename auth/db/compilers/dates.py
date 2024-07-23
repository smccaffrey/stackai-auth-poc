# type: ignore
from sqlalchemy import DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression


# pylint: disable=invalid-name
class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(*_, **__):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
