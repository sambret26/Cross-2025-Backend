from repositories.SettingRepository import SettingRepository
from repositories.ChannelRepository import ChannelRepository
from repositories.RunnerRepository import RunnerRepository
from logger.logger import log, HANDLE, MAIL
from constants import messages, settings
from models.Runner import Runner
from word import wordHandler
from mail import mailSender

settingRepository = SettingRepository()
channelRepository = ChannelRepository()
runnerRepository = RunnerRepository()

async def updateResultMessage(bot):
    channelId = channelRepository.getResultChannelId()
    channel = bot.get_channel(channelId)
    rewards = getRewards()
    await checkRewards(channel, rewards)
    async for message in channel.history(limit=100):
        if message.content.startswith("Nombre"):
            count = runnerRepository.count()
            number = settingRepository.getRunnerNumber()
            if count == None or number == None:
                log.error(HANDLE, messages.COUNT_ERROR)
                return
            arrived = str(count.value)
            total = str(number.value)
            newMessage = createRecapMessage(arrived, total, rewards)
            await message.edit(content=newMessage)
            return

async def checkRewards(channel, rewards):
    rewardInDB = settingRepository.getRewardsNumber()
    if rewardInDB == None:
        await channel.send(messages.ERROR_REWARD)
        return
    rewardNumbersInDB = rewardInDB.value
    rewardsNumber = 0
    for reward in rewards:
        if reward[1].last_name != None:
            rewardsNumber+=1
    if rewardsNumber == rewardNumbersInDB:
        return
    settingRepository.setRewardsNumbers(rewardsNumber)
    totalRewardsCounter = settingRepository.getTotalRewardsCounter()
    if totalRewardsCounter == None:
        log.error(HANDLE, messages.ERROR_TOTAL_REWARD)
        return
    if rewardsNumber != totalRewardsCounter.value:
        return
    wordHandler.createWordFile(rewards)
    toAdress = mailSender.sendMail()
    if toAdress == None:
        log.error(MAIL, f"{messages.ERROR_SENDING_MAIL} : {e}")
        await channel.send(messages.ERROR_SENDING_MAIL)
        return
    await channel.send(messages.ALL_REWARDS_KNOWN.replace("TO_ADRESS", toAdress))

def createRecapMessage(arrived, total, rewards):
    headers = settings.HEADERS
    colWidth = [len(header) for header in headers]
    for reward in rewards:
        if reward[1].last_name == None:
            continue
        for index, item in enumerate(reward): # TODO
            colWidth[index] = max(colWidths[index], len(str(item)))
    rowFormat = " | ".join(f"{{:<{width}}}" for width in colWidth)
    table = []
    table.append(rowFormat.format(*headers))
    table.append("-+-".join("-" * width for width in colWidth))
    for reward in rewards:
        if reward[1].last_name == None:
            continue
        table.append(rowFormat.format(*reward)) #TODO
    message = messages.RESULT.replace("ARRIVED", arrived).replace("TOTAL", total)
    message += messages.REWARDS_LIST
    message += "```\n" + "\n".join(table) + "\n```\n"
    message += Config.TO_SEND_MAIL
    return message
    
def getRewards():
    rewards = []
    for i in range(1, 6):
        category = "S" + str(i)
        runner = runnerRepository.getRewardInScratch(i, "M")
        if runner == None : runner = Runner()
        rewards.append((category, runner))
    for i in range(1, 4):
        category = "S" + str(i)
        runner = runnerRepository.getRewardInScratch(i, "F")
        if runner == None : runner = Runner()
        rewards.append((category, runner))
    for category in settings.CATEGORY_F:
        runner = runnerRepository.getRewardInCategoryF(category)
        if runner == None : runner = Runner()
        rewards.append((category, runner))
    for category in settings.CATEGORY_M:
        runner = runnerRepository.getRewardInCategoryM(category)
        if runner == None : runner = Runner()
        rewards.append((category, runner))
    bibNumberRewarded = [reward[1].bib_number for reward in rewards if reward[1].bib_number is not None]
    runner = runnerRepository.getFirstOriol("F", bibNumberRewarded)
    if runner == None : runner = Runner()
    rewards.append(("O", runner))
    runner = runnerRepository.getFirstOriol("M", bibNumberRewarded)
    if runner == None : runner = Runner()
    rewards.append(("O", runner))
    return(rewards)