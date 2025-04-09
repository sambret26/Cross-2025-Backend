from flask_sqlalchemy import SQLAlchemy
from pytz import timezone

from config import Config

db = SQLAlchemy()

timezone = timezone(Config.TIME_ZONE)