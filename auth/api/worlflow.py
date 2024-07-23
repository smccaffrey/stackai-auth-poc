"""
Workflow: A workflow can be thought of as a program that can be edited by users with editor permissions and run by users with viewer/external user permissions, depending on whether the workflow is exported to the public or not. Endpoints for this include:

- List all workflows that a user has access to.
- Create/Update new workflow.
- Execute worflow
- Execute exported workflow
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from auth.api.router import AuthRouter
from auth.helper import role_required 
from auth.enums import OrgRoles, TeamRoles
from auth.schemas.base import BaseRequest

from auth.api.deps.db import get_db


workflow_router = AuthRouter()


@workflow_router.get("/list")
@role_required(org_roles=[OrgRoles.MEMBER], team_roles=[TeamRoles.VIEWER])
async def list_worflows(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access to /list worflows"}


@workflow_router.put("/flow")
@role_required(org_roles=[OrgRoles.MEMBER], team_roles=[TeamRoles.EDITOR])
async def create_or_update_workflow(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access to /flow create or update worflows"}


@workflow_router.post("/execute")
@role_required(org_roles=[OrgRoles.MEMBER], team_roles=[TeamRoles.VIEWER])
async def execute(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access to /execute worflows"}


@workflow_router.post("/external/execute")
@role_required(team_roles=[TeamRoles.EXTERNAL_USER])
async def execute_external(
    request: BaseRequest,
    db_session: Session = Depends(get_db)
):
    return {"User has access to /external/execute worflows"}

