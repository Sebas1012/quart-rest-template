from dotenv import load_dotenv, find_dotenv
from datetime import timedelta
import os

load_dotenv(find_dotenv())

class Config:
    TORTOISE_DATABASE_URI           = os.environ.get('DB_URI')
    JWT_ACCESS_TOKEN_EXPIRES        = timedelta(minutes=30)
    SESSION_REFRESH_EACH_REQUEST    = True
    JWT_SECRET_KEY                  = os.environ.get('JWT_KEY')