from flask_cors import CORS
from flask import Flask
import threading

from services.controllers.RunnerController import runnerBp
from discord import discordController
from config import Config
from database import db

# Pour importer sans Blueprint
from models.Setting import Setting
from models.Channel import Channel

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
db.init_app(app)

# Registering blueprints
app.register_blueprint(runnerBp)

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