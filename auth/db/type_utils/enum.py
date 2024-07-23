# type: ignore

import sqlalchemy

from auth.db.constants import ENUM_STRING_MAX_LENGTH


class SqlAlchemyEnumError(BaseException):
    """Raised when there is an error casting an enum from the DB"""
    def __init__(self, message: str) -> None:  # pylint: disable=super-init-not-called
        self.message = message


# pylint: disable=abstract-method
class EnumAsString(sqlalchemy.types.TypeDecorator):
    """Column type for storing Python enums in a database STRING column.

    This will behave erratically if a database value does not correspond to
    a known enum value.
    """

    impl = sqlalchemy.types.VARCHAR  # underlying database type

    def __repr__(self):
        return (
            f"EnumAsString(length={ENUM_STRING_MAX_LENGTH}, "
            f"enum_type={self.enum_type.__name__})"
        )

    def __init__(self, enum_type, length=ENUM_STRING_MAX_LENGTH, use_value=True):
        super().__init__(length)
        self.enum_type = enum_type
        self.use_value = use_value
        if use_value:
            self.values_map = {k.value: k for k in enum_type}

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, self.enum_type):
            return value.value if self.use_value else value.name
        raise SqlAlchemyEnumError(
            f"Expected Enum {self.enum_type.__name__}, "
            f"got {value.__class__.__name__}"
        )

    def process_literal_param(self, value, dialect):
        return self.process_bind_param(value, dialect)

    def process_result_value(self, value, dialect):
        if value is None:
            return None

        if self.use_value:
            if value not in self.values_map:
                raise SqlAlchemyEnumError(
                    f"Value {value} not supported by "
                    f"{self.enum_type.__name__}. "
                    f"Supported values: {self.values_map.keys()}"
                )
            return self.values_map[value]

        if value not in self.enum_type.__members__:
            raise SqlAlchemyEnumError(
                f"Value {value} not supported by "
                f"{self.enum_type.__name__}. "
                f"Supported values: {self.enum_type.__members__}"
            )
        return self.enum_type[value]

    def copy(self, **_):
        return EnumAsString(self.enum_type, use_value=self.use_value)