from typing import TypeVar, Type, Generic, List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from auth.models.base import Base, BaseQuery  # type: ignore

ModelType = TypeVar("ModelType", bound=Base)


class BaseManager(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    # pylint: disable=redefined-builtin,invalid-name
    def get(self, db_session: Session, id: UUID) -> Optional[ModelType]:
        return db_session.query(self.model).filter(self.model.id == id).first()  # type: ignore

    def get_multi(
        self, db_session: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db_session.query(self.model).offset(skip).limit(limit).all()  # type: ignore

    def only(self, db_session: Session, fields: List[str]) -> BaseQuery:
        """
        Only select the passed in list of fields
        """
        # Incompatible return value type (got "Query[Any]", expected "BaseQuery")
        return db_session.query(*[getattr(self.model, f) for f in fields])