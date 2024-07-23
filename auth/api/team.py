"""
Teams:

- Create a team
- List teams a user belongs to and his role within them
- Add user to team
- Remove user from team
"""
from fastapi import Depends
from sqlalchemy.orm import Session

from auth.api.router import AuthRouter
from auth.helper import role_required 
from auth.enums import OrgRoles, TeamRoles
from auth.schemas.base import BaseRequest

from auth.api.deps.db import get_db


team_router = AuthRouter()


@team_router.post("/create")
@role_required(org_roles=[OrgRoles.SUPER_ADMIN], team_roles=[TeamRoles.ADMIN])
async def create_team(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access to /create"}

@team_router.get("/user-with-roles")
@role_required(org_roles=[OrgRoles.SUPER_ADMIN], team_roles=[TeamRoles.EDITOR])
async def user_with_roles(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access to /user-with-roles"}

@team_router.put("/add-user")
@role_required(org_roles=[OrgRoles.SUPER_ADMIN], team_roles=[TeamRoles.EDITOR])
async def add_user_to_team(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access to /add-user"}

@team_router.delete("/remove-user")
@role_required(org_roles=[OrgRoles.SUPER_ADMIN], team_roles=[TeamRoles.EDITOR])
async def remove_user_from_team(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access to /remove-use"}
