from models.Channel import Channel

class ChannelRepository:

    #GETTERS
    @staticmethod
    def getChannelId(category):
        channel = Channel.query.filter_by(category=category).first()
        if channel == None:
            return None
        return channel.channel_id