from supabase import create_client, Client
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
url = getenv("SUPABASE_URL", "https://your-project.supabase.co")
key = getenv("SUPABASE_KEY", "your-anon-key")

supabase: Client = create_client(url, key)


def client_db():
    """Access client table"""
    return supabase.table("client")


def notification_db():
    """Access notification table"""
    return supabase.table("notification")


def command_db():
    """Access command table"""
    return supabase.table("command")


def auth_db():
    """Access auth table"""
    return supabase.table("auth")


async def tear_drive():
    """Access storage bucket (if needed)"""
    return supabase.storage.from_("teardroid")
