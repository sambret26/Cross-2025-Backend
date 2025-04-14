from discord.ext import commands
from discord import Intents

from repositories.SettingRepository import SettingRepository
from logger.logger import log, BOT, DISCORD
from discord import discordBusiness
from constants import messages
from config import Config

settingRepository = SettingRepository()

DISCORD_GUILD_ID = int(Config.DISCORD_GUILD_ID)

intent = Intents(messages=True, members=True, guilds=True, reactions=True, message_content=True)
bot = commands.Bot(command_prefix='$', description='Cross 15 Août 2025', intents=intent)

@bot.command()
async def mail(ctx):
    await discordBusiness.mail(ctx)

@bot.command()
async def init(ctx):
    await discordBusiness.init(ctx)

@bot.command()
async def test(ctx):
    await discordBusiness.test(ctx)

@bot.command()
async def file(ctx):
    await discordBusiness.file(ctx)

@bot.command()
async def fromAdress(ctx, *args):
    await discordBusiness.fromAdress(ctx, args)

@bot.command()
async def toAdress(ctx, *args):
    await discordBusiness.toAdress(ctx, args)

@bot.command()
async def offsets(ctx, *args):
    await discordBusiness.offsets(ctx, args)

@bot.command()
async def totalRewards(ctx, *args):
    await discordBusiness.totalRewards(ctx, args)

@bot.command()
async def debug(ctx, *args):
    await discordBusiness.debug(ctx, args)

@bot.command()
async def cmd(ctx):
    await discordBusiness.cmd(ctx)

@bot.command()
async def clear(ctx, nombre: int = 100):
    await discordBusiness.clear(ctx, nombre)

@bot.event
async def on_ready():
    log.info(BOT, "Connected ! ")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.guild.id != DISCORD_GUILD_ID:
        return
    if message.attachments:
        await discordBusiness.importFile(bot, message)
    await bot.process_commands(message)

def main():
    debug = settingRepository.getValue('Debug')
    if debug == None:
        log.error(DISCORD, messages.DEBUG_ERROR)
        return
    if debug.value == "1":
        log.info(BOT, messages.DEBUG_START)
    else:
        log.info(BOT, messages.CLASSIC_START)
    bot.run(Config.DISCORD_TOKEN)