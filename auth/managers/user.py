from typing import Optional
from sqlalchemy.orm import Session
from auth.managers.base import BaseManager

from auth.models.orm.tables import User
from auth.models.user import UserResponse
from auth.schemas.user import UserCreate

from auth.models.orm.tables import user_organizations, user_teams

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
        else:
            db_obj = self.model(
                name=obj_in.name,
            )

        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)

        return db_obj

    def get_by_name(self, db_session: Session, name: str) -> Optional[UserResponse]:
        user = (
            db_session.query(self.model)
            .filter_by(name=name)
            .first()
        )

        if user:
            org_roles = db_session.query(user_organizations).filter_by(user_id=user.id).all()
            team_roles = db_session.query(user_teams).filter_by(user_id=user.id).all()
            
            return UserResponse(
                id=user.id,
                name=user.name,
                organizations=[{"organization_id": org.organization_id, "role": org.role} for org in org_roles],
                teams=[{"team_id": team.team_id, "role": team.role} for team in team_roles]
            )

        return None

users_manager = UsersManager(User)
