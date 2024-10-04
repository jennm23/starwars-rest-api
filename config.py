import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/starwars_blog')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
