from flask import Flask
import threading
from discord import discordController
from config import Config
from database import db
from flask_cors import CORS

# Pour importer sans Blueprint
from models.Runner import Runner
from models.Setting import Setting
from models.Channel import Channel

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
db.init_app(app)

def runDiscordBot():
    with app.app_context():
        discordController.main()

# Création des tables
with app.app_context():
    db.create_all()

discordThread = threading.Thread(target=runDiscordBot)
discordThread.start()

if __name__ == '__main__':
    app.run()