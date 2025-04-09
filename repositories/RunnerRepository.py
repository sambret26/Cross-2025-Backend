from models.Runner import Runner

from database import db


class RunnerRepository:
    
    # GETTERS
    @staticmethod
    def count():
        return Runner.query.count()

    @staticmethod
    def getRunnersForMap():
        return Runner.query.all()

    @staticmethod
    def getRewardInScratch(ranking, sex):
        return Runner.query.filter_by(sex_ranking=ranking, sex=sex).first()
    
    @staticmethod
    def getRewardInCategoryM(category):
        return Runner.query.filter(Runner.sex_ranking>5, Runner.sex=="M", Runner.category==category).order_by(Runner.category_ranking).first()
    
    @staticmethod
    def getRewardInCategoryF(category):
        return Runner.query.filter(Runner.sex_ranking>3, Runner.sex=="F", Runner.category==category).order_by(Runner.category_ranking).first()
    
    @staticmethod
    def getFirstOriol(sex, bibNumberRewarded):
        return Runner.query.filter(Runner.bib_number.notin_(bibNumberRewarded), Runner.sex==sex, Runner.oriol==True).order_by(Runner.sex_ranking).first()
    
    # ADDERS
    @staticmethod
    def addRunners(runners):
        db.session.add_all(runners)
        db.session.commit()
    
    # SETTERS
    @staticmethod
    def updateRunners(runners):
        db.session.bulk_update_mappings(Runner, runners)
        db.session.commit()
    
    # DELETERS
    @staticmethod
    def deleteAll():
        Runner.query.delete()
        db.session.commit()

