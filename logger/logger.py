import os
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))
log_timezone = timezone(os.getenv('TIME_ZONE'))

BOT = 'BOT'
CONFIG = '[CONFIG]'

class Log:
    def __init__(self):
        pass

    def info(self, logType, message):
        self.logPrint(f"[INFO] - {logType} - {message}")

    def warn(self, logType, message):
        self.logPrint(f"[WARN] - {logType} - {message}")

    def error(self, logType, message):
        self.logPrint(f"[ERROR] - {logType} - {message}")

    def logPrint(self, message):
        currentTime = datetime.now(log_timezone).strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{currentTime}] - {message}"
        print(message)

log = Log()