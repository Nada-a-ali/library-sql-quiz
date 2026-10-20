import os
from dotenv import load_dotenv
from supabase import create_client

# Load configuration
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Missing Supabase configuration")

# Initialize Supabase client
supabase = create_client(supabase_url, supabase_key)

print("Supabase client initialized successfully!")

# Test an actual network request
try:
    response = supabase.auth.get_session()
    print("Supabase Auth network request successful!")
    print("Current session:", "Signed in" if response else "Not signed in")
except Exception as error:
    print("Connection test failed:", error)
