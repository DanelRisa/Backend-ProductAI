from typing import Any
from pydantic import BaseSettings
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config(BaseSettings):
    CORS_ORIGINS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

    MONGOHOST: str = os.getenv("MONGOHOST", "localhost")
    MONGOPORT: str = os.getenv("MONGOPORT", "27017")
    MONGOUSER: str = os.getenv("MONGOUSER", "root")
    MONGOPASSWORD: str = os.getenv("MONGOPASSWORD", "password")
    MONGODATABASE: str = os.getenv("MONGODATABASE", "DanelProject")
    MONGO_URL: str = os.getenv("MONGO_URL", "")

# Environmental variables
env = Config()

# FastAPI configurations
fastapi_config: dict[str, Any] = {
    "title": "lolAPI",
}

mongo_url = (
    f"mongodb://{env.MONGOUSER}:{env.MONGOPASSWORD}@{env.MONGOHOST}:{env.MONGOPORT}/"
)
if env.MONGO_URL:
    mongo_url = env.MONGO_URL

# MongoDB connection
client = MongoClient(mongo_url)

# MongoDB database
database = client[env.MONGODATABASE]
