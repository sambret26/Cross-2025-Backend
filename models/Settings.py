from datetime import datetime

from database import db, timezone

class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String(50), nullable=False)
    state = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone))
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone), onupdate=datetime.now(timezone))