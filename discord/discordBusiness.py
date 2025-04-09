from repositories.SettingRepository import SettingRepository
from repositories.RunnerRepository import RunnerRepository
from discord import discordFunctions as functions
from constants import messages, settings
from logger.logger import log, MAIL
from word import wordHandler
from mail import mailSender
from config import Config
from gmcap import reader
import discord
import time

settingRepository = SettingRepository()
runnerRepository = RunnerRepository()

async def importFile(bot, message):
    file = await message.attachments[0].to_file()
    if not file.filename.endswith(".cap"):
        await message.channel.send(messages.UNKNOWN_FORMAT)
        return
    filename = settings.WORD_PATH + settings.GMCAP_FILENAME
    await message.attachments[0].save(filename)
    await sendFirstReact(message)
    start = time.time()
    await reader.handleFile(bot, filename)
    end = time.time()
    execution = end - start
    duration = f"{execution:.2f}"
    await sendSecondReact(message)
    await message.channel.send(messages.FILE_TREATED.replace("PC_NAME", Config.PC_NAME).replace("DURATION", duration))
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

async def file(ctx):
    rewards = functions.getRewards()
    wordHandler.createWordFile(rewards)
    file = discord.File(settings.WORD_PATH + settings.FINAL_WORD_FILENAME, filename = settings.FINAL_WORD_FILENAME)
    await ctx.send(messages.REWARD_FILE, file=file)

async def clear(ctx, nombre):
    await ctx.channel.purge(limit=nombre+1, check=lambda msg: not msg.pinned)

async def sendFirstReact(message):
    try:
        await message.add_reaction("🔄")
    except:
        None

async def sendSecondReact(message):
    try:
        await message.remove_reaction("🔄", bot.user)
    except:
        None
    try:
        await message.add_reaction("✅")
    except:
        None