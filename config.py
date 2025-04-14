import os
from dotenv import load_dotenv
from logger.logger import log, CONFIG

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    PC_NAME = os.getenv('PC_NAME')
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
    TIME_ZONE = os.getenv('TIME_ZONE')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    def __init__(self):
        if self.SQLALCHEMY_DATABASE_URI is None:
            log.warn(CONFIG, "DATABASE_URL is not set in .env file")