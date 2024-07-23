from fastapi import Request
from fastapi import APIRouter

from auth.api.router import AuthRouter

# from core_api.api.sources import sources_router
# from core_api.api.users import users_router
from auth.api.authenticate import authenticate_router
from auth.api.team import team_router


root_router: APIRouter = AuthRouter()

@root_router.get("/health")
@root_router.get("/")
def health_check() -> int:
    return 200

root_router.include_router(authenticate_router)
root_router.include_router(team_router, prefix="/team")
# root_router.include_router(sources_router, prefix="/v1/sources")
# root_router.include_router(users_router, prefix="/v1/users")