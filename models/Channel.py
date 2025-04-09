from datetime import datetime

from database import db, timezone

class Channel(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50))
    channel_id = db.Column(db.BigInteger)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone))
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone), onupdate=datetime.now(timezone))
