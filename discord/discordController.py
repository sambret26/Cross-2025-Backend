from config import Config
from discord import Intents
from discord.ext import commands
from discord import discordBusiness
from logger.logger import log, BOT

DISCORD_GUILD_ID = int(Config.DISCORD_GUILD_ID)

intent = Intents(messages=True, members=True, guilds=True, reactions=True, message_content=True)
bot = commands.Bot(command_prefix='$', description='Cross 15 Août 2025', intents=intent)

@bot.command()
async def check(ctx):
    await discordBusiness.check(ctx)

@bot.event
async def on_ready():
    log.info(BOT, "Connected ! ")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.guild.id != DISCORD_GUILD_ID:
        return
    await bot.process_commands(message)

def main():
    bot.run(Config.DISCORD_TOKEN)