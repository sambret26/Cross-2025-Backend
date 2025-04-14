from flask import Blueprint, jsonify

from repositories.RunnerRepository import RunnerRepository

runnerRepository = RunnerRepository()

runnerBp = Blueprint('runnerBp', __name__, url_prefix='/runners')

@runnerBp.route('/', methods=['GET'])
def getRunners():
    runners = runnerRepository.getRunners()
    return jsonify([runner.toDict() for runner in runners]), 200

@runnerBp.route('/<int:bibNumber>', methods=['GET'])
def getRunnerById(bibNumber):
    runner = runnerRepository.getByBibNumber(bibNumber)
    if runner == None : return jsonify({}), 404
    return jsonify(runner.toDict()), 200
