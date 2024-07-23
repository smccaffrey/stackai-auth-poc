import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.environ.get("ENV", "")
IS_TEST = ENV == "test"

DATABASE_URL = os.environ.get("{}DATABASE_URL".format("TEST_" if IS_TEST else ""))
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")