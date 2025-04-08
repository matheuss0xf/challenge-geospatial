import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    NOMINATIM_API = os.getenv('NOMINATIM_API')
    DATABASE = os.getenv('DATABASE')
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    DEBUG = os.getenv('DEBUG', 'False')