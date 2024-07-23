# type: ignore
from __future__ import annotations

import typing
import uuid

import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.orm import Query, Mapper
from sqlalchemy_mixins import (
    smart_query,
    SmartQueryMixin,
    ReprMixin,
    SerializeMixin,
    ModelNotFoundError,
)
from sqlalchemy_mixins.utils import classproperty

from auth import db
from auth.db.compilers.dates import utcnow
from auth.db.type_utils.dt import TZDateTime
from auth.db.type_utils.uuid import GUID


class BaseQuery(Query):
    # pylint: disable=E1101,E0213,R0201
    """
    BaseQuery class that can be used for custom, composable queries.
        All queries using the Model.where() syntax will be instances of BaseQuery.

    """

    def _get_models(self):
        """Returns the query's underlying model classes.
        Taken from https://stackoverflow.com/a/15962062
        """
        if hasattr(self, "attr"):
            # we are dealing with a subquery
            return [self.attr.target_mapper]
        return [
            d["expr"].class_
            for d in self.column_descriptions
            if isinstance(d["expr"], Mapper)
        ]

    def smart_query(self, filters=None, sort_attrs=None, schema=None):
        """
        Wrapper around sqlalchemy_mixins smart_query. This must be a public class
            to support more complex filters and sorts.
        """
        return smart_query(self, filters=filters, sort_attrs=sort_attrs, schema=schema)

    def where(self, **filters):  # pylint: disable=W0221
        """
        Mimics behavior of `Model.where()` from sqlalchemy_mixins to allow
            chainable `.where()` clauses.
        """
        return self.smart_query(filters=filters)

    def where_if_not_none(self, **filters):
        """
        Mimics behavior of `Model.where()` from sqlalchemy_mixins to allow
            chainable `.where()` clauses BUT removes "None" filter values.

        Useful for multi-filter queries where None-value searches need to be
        excluded.
        """
        filters = {key: value for (key, value) in filters.items() if value is not None}
        return self.smart_query(filters=filters)

    def sort(self, *columns):
        """
        Mimics behavior of `Model.sort()` from sqlalchemy_mixins to allow
            chainable `.sort()` clauses.
        """
        return self.smart_query(sort_attrs=columns)

    def only(self, *fields: typing.Any) -> BaseQuery:
        """
        Selects only the specified entities.
        """
        return self.with_entities(*fields)

    def find(self, id_):
        return self.get(id_)

    def find_or_fail(self, id_):
        # assume that query has custom get_or_fail method
        result = self.find(id_)
        if not result:
            raise ModelNotFoundError(f"id {id_} was not found")

        return result


class ClassMethodWarningMixin:
    @classmethod
    def where(cls, **filters):
        raise NotImplementedError("Use .query(db_session).where instead")

    @classmethod
    def sort(cls, *columns):
        raise NotImplementedError("Use .query(db_session).sort instead")

    @classmethod
    def smart_query(cls, filters=None, sort_attrs=None, schema=None):
        raise NotImplementedError("Use .query(db_session).smart_query instead")

    @classmethod
    def all(cls):
        raise NotImplementedError("Use .query(db_session).all instead")

    @classmethod
    def first(cls):
        raise NotImplementedError("Use .query(db_session).first instead")

    @classmethod
    def find(cls, id_):
        raise NotImplementedError("Use .query(db_session).find instead")

    @classmethod
    def find_or_fail(cls, id_):
        raise NotImplementedError("Use .query(db_session).find_or_fail instead")


# All features except ActiveRecordMixin
# Taken from sqlalchemy_mixins.__init__.py
class RefinementSQLAlchemyMixin(
    ClassMethodWarningMixin, SmartQueryMixin, ReprMixin, SerializeMixin
):
    __abstract__ = True
    __repr__ = ReprMixin.__repr__


class Base(db.DeclarativeBase, RefinementSQLAlchemyMixin):
    # pylint: disable=E1101,E0213,R0201
    __abstract__ = True

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(TZDateTime, server_default=utcnow(), nullable=True)
    last_updated = Column(
        TZDateTime, server_default=utcnow(), onupdate=utcnow(), nullable=True
    )

    def __repr__(self) -> str:
        return self._repr(id=self.id)

    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        """
        https://stackoverflow.com/a/55749579
        Helper for __repr__
        """
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                if key == "id":
                    field = str(field)
                field_strings.append(f"{key}={field!r}")
            except sa.orm.exc.DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({', '.join(field_strings)})>"
        return f"<{self.__class__.__name__} {str(self.id)}>"

    @classmethod
    def column_attrs(cls):
        """
        Helper method to return all column attributes of this table.
        """
        return [getattr(cls, col.key) for col in cls.__table__.columns]

    @classmethod
    def column_attrs_with_labels(cls):
        """
        Column attrs with "Model.field" labels on them for querying.
        """
        return [attr.label(f"{cls.__name__}.{attr.key}") for attr in cls.column_attrs()]

    # NOTE: Must use `from sqlalchemy_mixins.utils import classproperty`
    # instead of other implementations that don't lazily evaluate
    # the property. God knows why the sqlalchemy version does.
    @classmethod
    # pylint: disable=W0221
    def query(cls, session) -> BaseQuery:
        """
        A classproperty that returns an instantiated Query, ready to search.

        This method is overwriting source of sqlalchemy-mixins to make sure we choose
            the query_class cls.session is set with Base.set_session() and will raise
            an error if there's no session available.
        """
        return cls.query_cls(session)
        # return cls.query_cls(cls, session)

    @classproperty
    def query_cls(cls) -> BaseQuery:
        """
        The Query class used for particular queries. Each model may define its own.
        """
        return BaseQuery