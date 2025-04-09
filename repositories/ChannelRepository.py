from models.Channel import Channel

from database import db

class ChannelRepository:

    #GETTERS
    @staticmethod
    def getResultChannelId():
        return Channel.query.filter_by(category="Result").first().channel_id

    @staticmethod
    def getDebugChannelId():
        return Channel.query.filter_by(category="Debug").first().channel_id