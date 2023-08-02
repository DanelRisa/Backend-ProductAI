from pydantic import BaseSettings

from app.config import database

from .adapters.chatgpt_service import ChatGPTService
from .repository.repository import PostRepository

class Config(BaseSettings):
    OPENAI_API_KEY: str


class Service:
    def __init__(self):
        config = Config()    
        self.repository = PostRepository(database)
        self.chatgpt_service=ChatGPTService(config.OPENAI_API_KEY)


def get_service():
    svc = Service()
    return svc
