from models.Runner import Runner

from database import db


class RunnerRepository:
    
    # GETTERS
    @staticmethod
    def count():
        return Runner.query.count()

    @staticmethod
    def getIdByNameAndSurname(name, surname):
        return Runner.query.filter_by(name=name, surname=surname).first().id

    @staticmethod
    def getRewardInScratch(ranking, sex):
        return Runner.query.filter_by(ranking=ranking, sex=sex).first()
    
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
    def addRunner(runner):
        db.session.add(runner)
        db.session.commit()
    
    # SETTERS
    @staticmethod
    def updateRunner(runnerId, runner):
        Runner.query.filter_by(id=runnerId).update(runner.toDictForUpdate)
        db.session.commit()
    
    # DELETERS
    @staticmethod
    def deleteAll():
        Runner.query.delete()
        db.session.commit()

