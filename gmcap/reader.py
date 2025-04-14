from repositories.SettingRepository import SettingRepository
from repositories.ChannelRepository import ChannelRepository
from repositories.RunnerRepository import RunnerRepository
from discord.discordFunctions import replaceOffsetValues
from logger.logger import log, HANDLE, DEBUG
from models.Runner import Runner
from constants import messages

settingRepository = SettingRepository()
channelRepository = ChannelRepository()
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
    for _ in range (n):
        byte = file.read(1)
        if not byte : return -1
        value += chr(ord(byte))
    return value

def eatIntN(file, n):
    value = ""
    for _ in range (n):
        byte = file.read(1)
        if not byte : return -1
        value += str(ord(byte))
    return int(value)
            
def readWithLen(file):
    lenValue = file.read(1)
    length = ord(lenValue)
    return eatN(file, length)

def readIntWithLen(file):
    lenValue = file.read(1)
    length = ord(lenValue)
    return eatIntN(file, length)

def readIntWithFixLen(file, length):
    value = 0
    for compt in range (length):
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
    

def handle(runner, runnersMap, runnersToAdd, runnersToUpdate):
    if runner.ranking == 0 : return
    runnerInDB = runnersMap.get(runner.last_name + "_" + runner.first_name)
    if runnerInDB != None:
        if runner.isDifferent(runnerInDB):
            runner.id = runnerInDB.id
            runnersToUpdate.append(getUpdateValue(runner, runnerInDB))
    else:
        runnersToAdd.append(runner)
    
async def findHour(a, b, c, offsets):
    if a==0 and b==0 and c==0 : return None
    if a==offsets[0] and b==offsets[1] and c==offsets[2] : return None
    heures = 0
    minutes = 0
    if a < offsets[0]:
        secondes = 65536+a-offsets[0]
    else:
        secondes = a-offsets[0]
    if b > offsets[1]:
        secondes = secondes + 65536*(b-offsets[1]-1)
    if c < offsets[2]:
        milisecondes = 1000+c-offsets[2]
        secondes = secondes - 1
    else :
        milisecondes = c-offsets[2]
    while(secondes > 59):
        secondes = secondes - 60
        minutes = minutes + 1 
    while(minutes > 59):
        minutes = minutes - 60
        heures = heures + 1
    return(f'{heures:02}:{minutes:02}:{secondes:02}.{milisecondes:03}')

def createRunnersMap():
    runnersInDB = runnerRepository.getRunnersForMap()
    runnersMap = {}
    for runner in runnersInDB:
        runnersMap[runner.last_name + "_" + runner.first_name] = runner
    return runnersMap

def getUpdateValue(runner, runnerInDB):
    return {
        'id': runner.id,
        'first_name': runner.first_name,
        'last_name': runner.last_name,
        'sex': runner.sex,
        'ranking': runner.ranking,
        'category': runner.category,
        'category_ranking': runner.category_ranking,
        'sex_ranking': runner.sex_ranking,
        'bib_number': runner.bib_number,
        'time': runner.time,
        'oriol': runner.oriol or runnerInDB.oriol
    }

async def handleDebug(bot, a, b, c):
    channelId = channelRepository.getChannelId("Debug")
    if channelId == None:
        log.error(HANDLE, messages.CHANNEL_ERROR)
        return
    channel = bot.get_channel(channelId)
    message = replaceOffsetValues(messages.OFFSETS, [a, b, c])
    await channel.send(message)
    log.info(DEBUG, message)

def readMultiple(file, number):
    for _ in range(number):
        readWithLen(file) # Skip

async def handleFile(bot, filename):
    with open(filename, 'rb') as file:
        eatUntil(file, [b'\x00']*100)
        eatZero(file)
        number = readIntWithFixLen(file, 2)
        if number == 0 :
            return
        settingRepository.setValue('RunnerNumber', number)
        offsetsInDb = settingRepository.getValue('Offsets')
        if offsetsInDb == None:
            log.error(HANDLE, messages.ERROR_OFFSET)
            return None
        debug = settingRepository.getValue('Debug')
        if debug == None:
            log.error(HANDLE, messages.DEBUG_ERROR)
            return
        offsets = list(map(int, offsetsInDb.value.split(",")))
        runnersMap = createRunnersMap()
        runnersToAdd = []
        runnersToUpdate = []
        for _ in range(number):
            last_name = readWithLen(file).upper()
            first_name = readWithLen(file).title()
            sex = getSex(eatIntN(file, 1))
            file.read(1) # Skip
            bib_number = readIntWithFixLen(file,2)
            file.read(2) # Skip
            category = getCategory(eatIntN(file, 1))
            file.read(1) # Skip
            readWithLen(file) # Skip
            readIntWithFixLen(file, 2)
            readMultiple(file, 4)
            a = readIntWithFixLen(file, 2)
            b = readIntWithFixLen(file, 2)
            c = readIntWithFixLen(file, 2)
            if debug.value == "1":
                await handleDebug(bot, a, b, c)
                return
            runnerTime = await findHour(a, b, c, offsets)
            file.read(66)
            readMultiple(file, 2)
            file.read(8)
            readMultiple(file, 5)
            file.read(20)
            ranking = readIntWithFixLen(file,2)
            category_ranking = readIntWithFixLen(file,2)
            sex_ranking = readIntWithFixLen(file,2)
            readMultiple(file, 2)
            file.read(1)
            organism = readWithLen(file) #Skip
            readMultiple(file, 3)
            file.read(6)
            readWithLen(file)
            file.read(3)
            readWithLen(file)
            #file.read(1026)
            eatZero(file)
            file.read(1) # Attention !! Différent en fonction des fichiers
            eatZero(file) # Attention !! Différent en fonction des fichiers
            oriol = (organism.title() == "Oriol")
            runner = Runner(last_name, first_name, sex, ranking, category, category_ranking, sex_ranking, bib_number, runnerTime, oriol)
            if runnerTime != None :
                handle(runner, runnersMap, runnersToAdd, runnersToUpdate)
        runnerRepository.addRunners(runnersToAdd)
        runnerRepository.updateRunners(runnersToUpdate)
