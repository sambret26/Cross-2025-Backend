from datetime import datetime

from database import db, timezone

class Runner(db.Model):
    __tablename__ = 'runners'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    ranking = db.Column(db.Integer)
    category = db.Column(db.String(10), nullable=False)
    category_ranking = db.Column(db.Integer)
    sex_ranking = db.Column(db.Integer)
    bib_number = db.Column(db.Integer)
    time = db.Column(db.String(30))
    oriol = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone))
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone), onupdate=datetime.now(timezone))
