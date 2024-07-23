from fastapi import APIRouter

from auth.api.router import AuthRouter

from auth.api.authenticate import authenticate_router
from auth.api.team import team_router
from auth.api.organization import organization_router
from auth.api.worlflow import workflow_router


root_router: APIRouter = AuthRouter()

@root_router.get("/health")
@root_router.get("/")
def health_check() -> int:
    return 200

root_router.include_router(authenticate_router)
root_router.include_router(team_router, prefix="/team")
root_router.include_router(organization_router, prefix="/organization")
root_router.include_router(workflow_router, prefix="/workflow")
