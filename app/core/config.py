from dotenv import load_dotenv
import os

load_dotenv()

def get_env_variable(var_name, default=None):
    """Get an environment variable or return a default value."""
    return os.getenv(var_name, default)

DB_USER = get_env_variable("DB_USER")
DB_PASSWORD = get_env_variable("DB_PASSWORD")
DB_HOST = get_env_variable("DB_HOST")
DB_PORT = get_env_variable("DB_PORT", "5432")
DB_NAME = get_env_variable("DB_NAME")

SECRET_KEY = get_env_variable("SECRET_KEY")
ALGORITHM = get_env_variable("ALGORITHM")
ISS = get_env_variable("ISS", "myapp")
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env_variable("ACCESS_TOKEN_EXPIRE_MINUTES", 60))