from config import Config
from discord import Intents
from discord.ext import commands
from discord import discordBusiness
from logger.logger import log, BOT
from constants import messages

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
    if Config.DEBUG:
        log.info(BOT, messages.DEBUG_START)
    else:
        log.info(BOT, messages.CLASSIC_START)
    bot.run(Config.DISCORD_TOKEN)