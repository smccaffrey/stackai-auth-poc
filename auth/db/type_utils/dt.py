# type: ignore
from sqlalchemy import DateTime


class TZDateTime(DateTime):

    # pylint: disable=W0613,W1113
    def __init__(self, timezone=True, *args, **kwargs):
        super().__init__(timezone=True, *args, **kwargs)
