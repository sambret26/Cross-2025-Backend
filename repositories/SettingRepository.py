from models.Setting import Setting
from database import db

class SettingRepository:

    # GETTERS
    @staticmethod
    def getValue(key):
        return Setting.query.filter_by(key=key).first()
    
    # SETTERS
    @staticmethod
    def setValue(key, value):
        Setting.query.filter_by(key=key).update({'value': value})
        db.session.commit()