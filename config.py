import os
from dotenv import load_dotenv

load_dotenv()

def get_env_or_default(key, default=None, cast_func=str):
    value = os.getenv(key)
    if value is not None and value.strip() != "":
        try:
            return cast_func(value)
        except (ValueError, TypeError) as e:
            print(f"Error casting {key} with value '{value}' to {cast_func.__name__}: {e}")
            return default
    return default

API_ID = get_env_or_default("API_ID", "Your_API_ID_Here")
API_HASH = get_env_or_default("API_HASH", "Your_API_HASH_Here")
BOT_TOKEN = get_env_or_default("BOT_TOKEN", "Your_BOT_TOKEN_Here")
OWNER_ID = get_env_or_default("OWNER_ID", "Your_OWNER_ID_Here", int)
DEVELOPER_USER_ID = get_env_or_default("DEVELOPER_USER_ID", "Your_DEVELOPER_USER_ID_Here", int)
MONGO_URL = get_env_or_default("MONGO_URL", "Your_MONGO_URL_Here")
CC_GEN_LIMIT = get_env_or_default("CC_GEN_LIMIT", 2000, int)
MULTI_CCGEN_LIMIT = get_env_or_default("MULTI_CCGEN_LIMIT", 5000, int)
BIN_KEY = get_env_or_default("BIN_KEY", "Your_BIN_KEY_Here")

raw_prefixes = get_env_or_default("COMMAND_PREFIX", "!|.|#|,|/")
COMMAND_PREFIX = [prefix.strip() for prefix in raw_prefixes.split("|") if prefix.strip()]
UPDATE_CHANNEL_URL = get_env_or_default("UPDATE_CHANNEL_URL", "t.me/TheSmartDev")

required_vars = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "OWNER_ID": OWNER_ID,
    "MONGO_URL": MONGO_URL
}

for var_name, var_value in required_vars.items():
    if var_value is None or var_value == f"Your_{var_name}_Here" or (isinstance(var_value, str) and var_value.strip() == ""):
        raise ValueError(f"Required variable {var_name} is missing or invalid. Set it in .env (VPS), config.py (VPS), or Heroku config vars.")

print("Loaded COMMAND_PREFIX:", COMMAND_PREFIX)

if not COMMAND_PREFIX:
    raise ValueError("No command prefixes found. Set COMMAND_PREFIX in .env, config.py, or Heroku config vars.")
