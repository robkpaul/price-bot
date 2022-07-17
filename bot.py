import logging
import os
import sqlite3
import sys
from cogs.reg import Reg
from cogs.cron import Cron
from disnake import Intents
from disnake.ext import commands
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, 
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("bot")

env = load_dotenv()
token = os.environ.get("DISCORD_TOKEN")

db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()
cursor.execute('''DROP TABLE IF EXISTS games''')
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS games  (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        game_id INTEGER NOT NULL,
        channel INTEGER NOT NULL,
        registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );'''
)

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(
    sync_commands=True,
    intents=intents,
)

@bot.listen("on_ready")
async def readied():
    logger.info(f"Logged in as {bot.user}")

bot.add_cog(Reg(bot, db))
bot.add_cog(Cron(bot, db))
bot.run(token)