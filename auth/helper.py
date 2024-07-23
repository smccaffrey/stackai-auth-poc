from typing import List, Dict

from functools import wraps
from fastapi import HTTPException
from sqlalchemy.orm import Session

from auth.schemas.base import BaseRequest
from auth.enums import OrgRoles, TeamRoles
from auth.services.supabase import supabase
from auth.managers.user import users_manager
from auth.models.user import UserResponse



ALLOWED_ROLE_OVERLAP: Dict[OrgRoles | TeamRoles, List[OrgRoles | TeamRoles]] = {
    OrgRoles.SUPER_ADMIN.name: [
        OrgRoles.MEMBER
    ],
    OrgRoles.MEMBER.name: [],
    TeamRoles.ADMIN.name: [
        TeamRoles.EDITOR,
        TeamRoles.VIEWER,
        TeamRoles.EXTERNAL_USER
    ],
    TeamRoles.EDITOR.name: [
        TeamRoles.VIEWER,
        TeamRoles.EXTERNAL_USER
    ],
    TeamRoles.EXTERNAL_USER.name: [],
    TeamRoles.VIEWER.name: [],
}

def role_required(org_roles: List[OrgRoles] = [], team_roles: List[TeamRoles] = []):
    def role_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            
            # external endpoints should return immediately
            if team_roles == [TeamRoles.EXTERNAL_USER]:
                return await func(*args, **kwargs)


            db_session: Session = kwargs.get("db_session")
            request: BaseRequest = kwargs.get("request")
            access_token: str = request.access_token

            supabase_user_id: str = supabase.auth.get_user(access_token).user.id

            user: UserResponse = users_manager.get_by_name(
                db_session=db_session,
                name=supabase_user_id
            )
            user_org_roles: List[OrgRoles] = [
                user.organizations[0].role,
            ] + ALLOWED_ROLE_OVERLAP[user.organizations[0].role.name]

            user_team_roles: List[TeamRoles] = [
                user.teams[0].role,
            ] + ALLOWED_ROLE_OVERLAP[user.teams[0].role.name]


            has_org_access: bool = any(role in org_roles for role in user_org_roles)
            has_team_access: bool = any(role in team_roles for role in user_team_roles)
            if has_org_access or has_team_access:
                return await func(*args, **kwargs)
            raise HTTPException(status_code=403, detail="Insufficient permissions")
            
        return wrapper
    return role_decorator