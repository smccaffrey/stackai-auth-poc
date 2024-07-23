from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from auth.managers.base import BaseManager
from auth.models.orm.tables import User
from auth.schemas.user import UserCreate, UserUpdate

class UsersManager(BaseManager[User]):

    def create_or_update(
        self,
        db_session: Session,
        obj_in: UserCreate
    ) -> User:

        db_obj = (
            db_session.query(self.model)
            .filter_by(name=obj_in.name)
            .first()
        )

        if db_obj:
            db_obj.name = obj_in.name
            # Add any other fields that need to be updated
        else:
            db_obj = self.model(
                name=obj_in.name,
                # Add any other fields for the new user
            )

        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)

        return db_obj


users_manager = UsersManager(User)
