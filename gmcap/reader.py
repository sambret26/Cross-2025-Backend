from repositories.SettingRepository import SettingRepository
from repositories.RunnerRepository import RunnerRepository

from logger.logger import log, HANDLE
from constants import messages
from config import Config

settingRepository = SettingRepository()
runnerRepository = RunnerRepository()

def eatUntil(file, targetBytes):
    joinTargetBytes = b''.join(targetBytes)
    newTarget = bytearray(joinTargetBytes)
    targetLen = len(targetBytes)
    buffer = bytearray(targetLen)
    while True:
        byte = file.read(1)
        if not byte : break
        buffer.pop(0)
        buffer.append(byte[0])
        if buffer == newTarget : break
    
def eatZero(file):
    finish = False
    while not finish:
        byte = file.read(1)
        if not byte : return -1
        if byte != b'\x00':
            file.seek(-1, 1)
            finish = True
            
def eatN(file, n):
    value = ""
    for i in range (n):
        byte = file.read(1)
        if not byte : return -1
        value += chr(ord(byte))
    return value

def eatIntN(file, n):
    value = ""
    for i in range (n):
        byte = file.read(1)
        if not byte : return -1
        value += str(ord(byte))
    return int(value)
            
def readWithLen(file):
    lenValue = file.read(1)
    len = ord(lenValue)
    return eatN(file, len)

def readIntWithLen(file):
    lenValue = file.read(1)
    len = ord(lenValue)
    return eatIntN(file, len)

def readIntWithFixLen(file, len):
    value = 0
    for compt in range (len):
        value += eatIntN(file, 1) * (16**(compt*2))
    return value

def getSex(sexValue):
    if sexValue == 0 : return 'M'
    return 'F'

def getCategory(value):
    if value == 40 : return "J"
    if value == 41 : return "S"
    if value == 42 : return "35+"
    if value == 43 : return "45+"
    if value == 44 : return "55+"
    return "65+"
    

def handle(runner):
    if runner.ranking == 0 : return
    id = runnerRepository.getIdByNameAndSurname(runner.first_name, runner.last_name)
    if id != None:
        runnerRepository.updateRunner(id, runner)
    else:
        runnerRepository.addRunner(runner)
    
def findHour(a, b, c):
    if Config.DEBUG : print(a, b, c)
    if a==0 and b==0 and c==0 : return None
    offsetsInDb = settingRepository.getOffsets()
    if offsetsInDb == None:
        log.error(HANDLE, messages.ERROR_OFFSET)
        return None
    offsets = list(map(int, offsetsInDb.value.split(",")))
    offseta, offsetb, offsetc = offsets
    if a==offseta and b==offsetb and c==offsetc : return None
    heures = 0
    minutes = 0
    if a < offseta:
        secondes = 65536+a-offseta
    else:
        secondes = a-offseta
    if b > offsetb:
        secondes = secondes + 65536*(b-offsetb-1)
    if c < offsetc:
        milisecondes = 1000+c-offsetc
        secondes = secondes - 1
    else :
        milisecondes = c-offsetc
    while(secondes > 59):
        secondes = secondes - 60
        minutes = minutes + 1 
    while(minutes > 59):
        minutes = minutes - 60
        heures = heures + 1
    return(f'{heures:02}:{minutes:02}:{secondes:02}.{milisecondes:03}')

def handleFile(filename):
    with open(filename, 'rb') as file:
        eatUntil(file, [b'\x00']*100)
        eatZero(file)
        number = readIntWithFixLen(file, 2)
        if number > 0 : settingRepository.setRunnerNumber(number)
        for i in range(number):
            name = readWithLen(file).upper()
            surname = readWithLen(file).title()
            sex = getSex(eatIntN(file, 1))
            file.read(1) # Skip
            bib_number = readIntWithFixLen(file,2)
            file.read(2) # Skip
            category = getCategory(eatIntN(file, 1))
            file.read(1) # Skip
            readWithLen(file) # Skip
            readIntWithFixLen(file, 2)
            for j in range(4):
                readWithLen(file) # Skip
            a = readIntWithFixLen(file, 2)
            b = readIntWithFixLen(file, 2)
            c = readIntWithFixLen(file, 2)
            runnerTime = findHour(a, b, c)
            file.read(66)
            for j in range(2):
                readWithLen(file) # Skip
            file.read(8)
            for j in range(5):
                readWithLen(file) # Skip
            file.read(20)
            ranking = readIntWithFixLen(file,2)
            category_ranking = readIntWithFixLen(file,2)
            sex_ranking = readIntWithFixLen(file,2)
            for j in range(2):
                readWithLen(file) # Skip
            file.read(1)
            organism = readWithLen(file) #Skip
            for j in range(3):
                readWithLen(file) # Skip
            file.read(6)
            readWithLen(file)
            file.read(3)
            readWithLen(file)
            #file.read(1026)
            eatZero(file)
            file.read(1) # Attention !! Différent en fonction des fichiers
            eatZero(file) # Attention !! Différent en fonction des fichiers
            oriol = (organism.title() == "Oriol")
            runner = Runner(name, surname, sex, ranking, category, category_ranking, sex_ranking, bib_number, runnerTime, oriol)
            if runnerTime != None : handle(runner)