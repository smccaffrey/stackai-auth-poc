from pydantic import BaseModel
from typing import Optional

class BaseRequest(BaseModel):
    access_token: str


class BaseResponse(BaseModel):
    message: Optional[str] = None
    error: Optional[str] = None