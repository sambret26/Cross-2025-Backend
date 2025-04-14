from datetime import datetime

from database import db, timezone

class Runner(db.Model):
    __tablename__ = 'runners'

    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
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

    def __init__(self, first_name="", last_name="", sex="", ranking=0, category="", category_ranking=0, sex_ranking=0, bib_number=0, time="", oriol=False):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.ranking = ranking
        self.category = category
        self.category_ranking = category_ranking
        self.sex_ranking = sex_ranking
        self.bib_number = bib_number
        self.time = time
        self.oriol = oriol

    def toDict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'sex': self.sex,
            'ranking': self.ranking,
            'category': self.category,
            'category_ranking': self.category_ranking,
            'sex_ranking': self.sex_ranking,
            'bib_number': self.bib_number,
            'time': self.time,
            'oriol': self.oriol
        }

    def isDifferent(self, runner):
        return self.first_name != runner.first_name or \
            self.last_name != runner.last_name or \
            self.sex != runner.sex or \
            self.ranking != runner.ranking or \
            self.category_ranking != runner.category_ranking or \
            self.sex_ranking != runner.sex_ranking or \
            self.bib_number != runner.bib_number or \
            self.time != runner.time or \
            (self.oriol != runner.oriol and runner.oriol)