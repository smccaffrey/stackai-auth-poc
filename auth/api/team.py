"""
Teams:

- Create a team
- List teams a user belongs to and his role within them
- Add user to team
- Remove user from team
"""

from auth.api.router import AuthRouter
# from auth.schemas.team import 


team_router = AuthRouter()


@team_router.post("/create")
async def create_team():
    pass

@team_router.get("/user-with-roles")
async def user_with_roles():
    pass

@team_router.put("/add-user")
async def add_user_to_team():
    pass

@team_router.delete("/remove-user")
async def remove_user_from_team():
    pass