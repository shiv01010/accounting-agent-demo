import os
from supabase import create_client, Client


url: str = os.getenv("SUPABASE_URL", "https://your-supabase-url.supabase.co")
key: str = os.getenv("SUPABASE_API_KEY", "your-supabase-key")

supabase: Client = create_client(url, key)


def get_supabase_client() -> Client:
    """Returns the Supabase client."""
    return supabase
