import os

class Config:
    SECRET_KEY = 'your-secret-key-123-alcohol-mvc'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///alcohol_mvc.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True