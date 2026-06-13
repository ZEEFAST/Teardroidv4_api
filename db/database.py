from supabase import create_client, Client
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
url = getenv("SUPABASE_URL")
key = getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required!")

supabase: Client = create_client(url, key)

def get_supabase():
    """Get Supabase client instance"""
    return supabase

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

def storage():
    """Access storage bucket"""
    return supabase.storage.from_("zeefer-droid")
