from fastapi import APIRouter

class AuthRouter(APIRouter):
    """Auth router"""
    def __init__(self) -> None:
        super().__init__()
