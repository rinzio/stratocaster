import os

ENV = os.getenv("APP_ENV", "dev").lower()

if ENV == "docker":
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017")
    MONGO_DB = os.getenv("MONGO_DB", "POC")
elif ENV == "dev":
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
    MONGO_DB = os.getenv("MONGO_DB", "POC")
