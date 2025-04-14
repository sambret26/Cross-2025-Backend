from models.Setting import Setting
from database import db

class SettingRepository:
    # ADDERS
    @staticmethod
    def addValue(key, value):
        newSetting = Setting(key=key, value=value)
        db.session.add(newSetting)
        db.session.commit()

    # GETTERS
    @staticmethod
    def getValue(key):
        return Setting.query.filter_by(key=key).first()
    
    # SETTERS
    @staticmethod
    def setValue(key, value):
        Setting.query.filter_by(key=key).update({'value': value})
        db.session.commit()