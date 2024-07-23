import requests

from gotrue.types import AuthResponse

from auth.services.supabase import supabase
from auth.settings import SUPABASE_URL, SUPABASE_KEY

# TODO: Wrap all these functions in a class and export as singleton

async def _login(email: str, password: str):
    response: AuthResponse = supabase.auth.sign_in_with_password({ "email": email, "password": password })
    return response.session.access_token, response.user.id


async def _logout(token: str) -> bool:
    url = f"{SUPABASE_URL}/auth/v1/logout"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    print(response)
    if response.status_code != 200:
        return False
    return True

async def _validate_token(access_token: str) -> bool:
    response = supabase.auth.get_user(access_token)
    return response.user.aud == 'authenticated'

async def _sign_up(email: str, password: str):
    response = supabase.auth.sign_up(
        credentials={"email": f"{email}", "password": "{password}"}
    )
    if response.user.id:
        return response.user.id
