from pydantic import BaseModel

from auth.schemas.base import BaseRequest
from auth.schemas.base import BaseResponse

class TeamCreateRequest(BaseRequest):
    name: str


class TeamCreateResponse(BaseResponse):
    pass


class TeamAddUserRequest(BaseRequest):
    pass


class TeamAddUserResponse(BaseResponse):
    pass