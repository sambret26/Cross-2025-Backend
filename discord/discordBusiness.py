import discord
import time

from repositories.SettingRepository import SettingRepository
from repositories.RunnerRepository import RunnerRepository
from discord import discordFunctions as functions
from logger.logger import log, MAIL, DISCORD
from constants import messages, settings
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
    filename = settings.WORD_PATH + settings.GMCAP_FILENAME
    await message.attachments[0].save(filename)
    await sendFirstReact(message)
    start = time.time()
    await reader.handleFile(bot, filename)
    end = time.time()
    execution = end - start
    duration = f"{execution:.2f}"
    await sendSecondReact(bot, message)
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
        return

async def init(ctx):
    runnerRepository.deleteAll()
    settingRepository.setValue('RunnerNumber', 0)
    settingRepository.setValue('RewardsNumber', 0)
    await ctx.send(messages.DB_INIT)

async def test(ctx):
    await ctx.send(messages.OK)

async def file(ctx):
    rewards = functions.getRewards()
    wordHandler.createWordFile(rewards)
    file = discord.File(settings.WORD_PATH + settings.FINAL_WORD_FILENAME, filename = settings.FINAL_WORD_FILENAME)
    await ctx.send(messages.REWARD_FILE, file=file)

async def fromAdress(ctx, args):
    if len(args) == 0 :
        fromAdress = settingRepository.getValue('FromAdress')
        if fromAdress == None:
            log.error(DISCORD, messages.ERROR_FETCHING_FROM_ADRESS)
            await ctx.send(messages.ERROR_FETCHING_FROM_ADRESS)
            return None
        await ctx.send(messages.FROM_ADRESS.replace("FROM_ADRESS", fromAdress.value))
    else:
        if not(functions.isCorrectEmail(args[0])):
            await ctx.send(messages.INVALID_ADRESS)
            return
        settingRepository.setValue('FromAdress', args[0])
        await ctx.send(messages.FROM_ADRESS_SET.replace("FROM_ADRESS", args[0]))

async def toAdress(ctx, args):
    if len(args) == 0 :
        toAdress = settingRepository.getValue('ToAdress')
        if toAdress == None:
            log.error(DISCORD, messages.ERROR_FETCHING_TO_ADRESS)
            await ctx.send(messages.ERROR_FETCHING_TO_ADRESS)
            return None
        await ctx.send(messages.TO_ADRESS.replace("TO_ADRESS", toAdress.value))
    else:
        if not(functions.isCorrectEmail(args[0])):
            await ctx.send(messages.INVALID_ADRESS)
            return
        settingRepository.setValue('ToAdress', args[0])
        await ctx.send(messages.TO_ADRESS_SET.replace("TO_ADRESS", args[0]))

async def offsets(ctx, args):
    if len(args) == 0 :
        offsets = settingRepository.getValue('Offsets')
        if offsets == None:
            log.error(DISCORD, messages.ERROR_FETCHING_OFFSET)
            await ctx.send(messages.ERROR_FETCHING_OFFSET)
            return None
        message = functions.getOffsetsMessages(offsets.value.split(','))
        await ctx.send(message)
        return
    offsets = functions.getOffsetsFromArgs(args)
    if offsets == None:
        await ctx.send(messages.INVALID_OFFSETS)
    else:
        offsetsValues = ",".join([str(offset) for offset in offsets])
        settingRepository.setValue('Offsets', offsetsValues)
        message = functions.replaceOffsetValues(messages.OFFSETS_SET, offsets)
        await ctx.send(message)

async def totalRewards(ctx, args):
    if len(args) == 0 :
        totalRewards = settingRepository.getValue('TotalRewardsCounter')
        if totalRewards == None:
            log.error(HANDLE, messages.ERROR_TOTAL_REWARD)
            await ctx.send(messages.ERROR_TOTAL_REWARD)
            return None
        await ctx.send(messages.TOTAL_REWARDS.replace("TOTAL_REWARDS", totalRewards.value))
        return
    if not(args[0].isdigit()):
        await ctx.send(messages.INVALID_REWARDS)
        return
    settingRepository.setValue('TotalRewardsCounter', args[0])
    await ctx.send(messages.TOTAL_REWARDS_SET.replace("TOTAL_REWARDS", args[0]))

async def debug(ctx, args):
    if len(args) == 0 or args[0].lower() == "on":
        settingRepository.setValue('Debug', '1')
        log.info(DISCORD, messages.DEBUG_ON)
        await ctx.send(messages.DEBUG_ON)
        return
    if args[0].lower() == "off":
        settingRepository.setValue('Debug', '0')
        log.info(DISCORD, messages.DEBUG_OFF)
        await ctx.send(messages.DEBUG_OFF)
        return
    await ctx.send(messages.INVALID_DEBUG)
    return

async def cmd(ctx):
    await ctx.send(messages.CMD)

async def clear(ctx, nombre):
    await ctx.channel.purge(limit=nombre+1, check=lambda msg: not msg.pinned)

async def sendFirstReact(message):
    try:
        await message.add_reaction("🔄")
    except:
        None

async def sendSecondReact(bot, message):
    try:
        await message.remove_reaction("🔄", bot.user)
    except:
        None
    try:
        await message.add_reaction("✅")
    except:
        None