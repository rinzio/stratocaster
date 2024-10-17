import os

ENV = os.getenv("APP_ENV", "dev").lower()
MONGO_DEFAULT = ""

if ENV == "docker":
    MONGO_DEFAULT = "mongodb://db:27017"
elif ENV == "dev":
    MONGO_DEFAULT = "mongodb://127.0.0.1:27017"

MONGO_URI = os.getenv("MONGO_URI", MONGO_DEFAULT)
MONGO_DB = os.getenv("MONGO_DB", "POC")


AUTH_SECRET_KEY = os.environ["AUTH_SECRET_KEY"]
AUTH_ALGORITHM = os.environ["AUTH_ALGORITHM"]
AUTH_EXPIRE = int(os.environ["AUTH_EXPIRE"])