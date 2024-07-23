"""
Organization:

- Add user to org
- Delete user from org
- Change org level role
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from auth.api.router import AuthRouter
from auth.helper import role_required 
from auth.enums import OrgRoles, TeamRoles
from auth.schemas.base import BaseRequest

from auth.api.deps.db import get_db


organization_router = AuthRouter()


@organization_router.put("/user")
@role_required(org_roles=[OrgRoles.SUPER_ADMIN])
async def add_user(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access put /user"}


@organization_router.delete("/user")
@role_required(org_roles=[OrgRoles.SUPER_ADMIN])
async def delete_user(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access to delete /user"}


@organization_router.delete("/user/role")
@role_required(org_roles=[OrgRoles.SUPER_ADMIN])
async def change_role(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access to change /user/role"}