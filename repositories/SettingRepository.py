from models.Setting import Setting

from database import db

class SettingRepository:

    # GETTERS
    @staticmethod
    def getRunnerNumber():
        return Setting.query.filter_by(key='RunnerNumber').first()

    @staticmethod
    def getRewardsNumber():
        return Setting.query.filter_by(key='RewardsNumber').first()

    @staticmethod
    def getTotalRewardsCounter():
        return Setting.query.filter_by(key='TotalRewardsCounter').first()
    
    @staticmethod
    def getFromAdress():
        return Setting.query.filter_by(key='FromAdress').first()
    
    @staticmethod
    def getToAdress():
        return Setting.query.filter_by(key='ToAdress').first()

    @staticmethod
    def getOffsets():
        return Setting.query.filter_by(key='Offsets').first()

    # SETTERS
    @staticmethod
    def setRunnerNumber(runnerNumber):
        Setting.query.filter_by(key='RunnerNumber').update({'value': runnerNumber})
        db.session.commit()

    @staticmethod
    def setRewardsNumbers(rewardsNumber):
        Setting.query.filter_by(key='RewardsNumber').update({'value': rewardsNumber})
        db.session.commit()
