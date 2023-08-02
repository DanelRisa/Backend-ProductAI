from pydantic import BaseSettings

from app.config import database

from .repository.repository import CartRepository

# class Config(BaseSettings):


class Service:
    def __init__(self):
        # config = Config()    
        self.repository = CartRepository(database)


def get_service():
    svc = Service()
    return svc
