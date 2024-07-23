from supabase import create_client, Client

from auth.settings import SUPABASE_URL, SUPABASE_KEY

# TODO: yield for dependency and session management
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)