from repositories.SettingRepository import SettingRepository
from repositories.RunnerRepository import RunnerRepository
from discord import discordFunctions as functions
from constants import messages, settings
from logger.logger import log, MAIL
from word import wordHandler
from mail import mailSender
from config import Config
from gmcap import reader

settingRepository = SettingRepository()
runnerRepository = RunnerRepository()

async def importFile(bot, message):
    file = await message.attachments[0].to_file()
    if not file.filename.endswith(".cap"):
        await message.channel.send(messages.UNKNOWN_FORMAT)
        return
    await message.attachments[0].save(settings.GMCAP_FILENAME)
    reader.handleFile(settings.GMCAP_FILENAME)
    await message.channel.send(messages.FILE_TREATED.replace("PC_NAME", Config.PC_NAME))
    await functions.updateResultMessage(bot)

async def mail(ctx):
    try:
        rewards = functions.getRewards()
        wordHandler.createWordFile(rewards)
        toAdress = mailSender.sendMail()
        if toAdress != None:
            await ctx.send(messages.MAIL_SENT.replace("TO_ADRESS", toAdress))
    except Exception as e:
        log.error(MAIL, f"{messages.ERROR_SENDING_MAIL} : {e}")
        await ctx.send(messages.ERROR_SENDING_MAIL)

async def init(ctx):
    runnerRepository.deleteAll()
    settingRepository.setRunnerNumber(0)
    settingRepository.setRewardsNumbers(0)
    await ctx.send(messages.DB_INIT)

async def test(ctx):
    await ctx.send(messages.OK)

async def clear(ctx, nombre):
    await ctx.channel.purge(limit=nombre+1, check=lambda msg: not msg.pinned)