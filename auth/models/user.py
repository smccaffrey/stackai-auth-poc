from pydantic import BaseModel
from typing import List

from auth.enums import OrgRoles, TeamRoles

class OrganizationRole(BaseModel):
    organization_id: int
    role: OrgRoles

class TeamRole(BaseModel):
    team_id: int
    role: TeamRoles

class UserBase(BaseModel):
    name: str

class UserResponse(UserBase):
    id: int
    organizations: List[OrganizationRole]
    teams: List[TeamRole]

    class Config:
        orm_mode = True
