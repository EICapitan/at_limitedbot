import os
import sys
import logging
from datetime import datetime

import discord
import psycopg2
import wavelink
import colorama
from discord.ext import commands

import embeds
from exceptions import FileError
from music import music_cog

print("AT PROJECT Limited, 2022 - 2024;  AT_nEXT-v3.6.3")
print("Product licensed by GPLv3, file `LICENSE`")
print("The license applies to all project files since ATLB-v3.2-gpl3")

# For development
# from dotenv import load_dotenv
# load_dotenv()

# Setting up custom formatter for handler
colorama.init(autoreset=True)
class ColoredFormatter(logging.Formatter):
    COLOR_MAP = {
        'DEBUG': colorama.Fore.BLUE,
        'INFO': colorama.Fore.GREEN,
        'WARN': colorama.Fore.YELLOW,
        'ERROR': colorama.Fore.RED,
        'CRIT': colorama.Fore.MAGENTA,
    }

    def format(self, record):
        if record.levelname == 'WARNING':
            record.levelname = 'WARN'

        if record.levelname == 'CRITICAL':
            record.levelname = 'CRIT'

        log_message = super().format(record)
        log_level_color = self.COLOR_MAP.get(record.levelname, colorama.Fore.WHITE)
        log_message = f"[{record.created:.1f}s] {log_level_color}[{record.levelname}]"\
                      f"{colorama.Style.RESET_ALL}\t- {log_message}"
        return log_message

# Setting up discord's logger to custom handler
time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
output_handler = logging.StreamHandler(sys.stdout)
output_handler.setFormatter(ColoredFormatter())
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger.addHandler(output_handler)

# Getting global variables
TOKEN  = os.environ['DISCORD_TOKEN']  # Discord token
PASSWD = os.environ['PASSWD']         # Lavalink password
LVHOST = os.environ['LVHOST']         # Lavalink host ip address
DBUSER = os.environ['DBUSER']         # PSQL database username  
DBPASS = os.environ['DBPASS']         # PSQL database password
DBHOST = os.environ['DBHOST']         # PSQL database host ip address


class Bot(commands.Bot):
    def __init__(self, commands_prefix, intents):
        super().__init__(command_prefix=commands_prefix, intents=intents)

    async def async_cleanup(self):
        await self.cogs['music_cog'].bot_cleanup()
    
    async def close(self):
        logger.info("Cleaning up...")
        await self.async_cleanup()
        logger.info("Shutting down")
        await super().close()


bot = Bot(commands_prefix = "sc.", intents=discord.Intents.all())
conn = psycopg2.connect(
        host = DBHOST,
        database = "nextmdb",
        user = DBUSER,
        password = DBPASS)
logger.info("Connected to PSQL database")

# Checking if environment variables are set
if None in [TOKEN, PASSWD, DBHOST, DBPASS, DBUSER]:
    raise(FileError('.env', 'corrupt'))
logger.info("Files checked")


# Bot configuration
@bot.event
async def on_ready():
    await bot.add_cog(music_cog(bot, conn, logger))
    await bot.change_presence(status=discord.Status.online, 
                              activity=discord.Game("Link, start.."))
    bot.dispatch("guilds_autosync") # Sending event to bot for update every guild's commands

    node: wavelink.Node = wavelink.Node(uri=f'http://{LVHOST}', password=PASSWD)
    await wavelink.Pool.connect(client=bot, nodes=[node])
    logger.info("Bot ready")
    

@bot.event
async def on_wavelink_node_ready(payload: wavelink.NodeReadyEventPayload):
    logger.info(f"Node \x1b[39;1mID: {payload.node.identifier}\x1b[39;0m ready.")


@bot.command()
async def inspect(ctx):
    await ctx.send(embed=embeds.default())

if __name__ == "__main__":
    bot.run(TOKEN, log_handler=None)
