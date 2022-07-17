import logging
import os
import sys

import aiosqlite
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

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(
    sync_commands=True,
    intents=intents,
)
bot.db_con = None

@bot.listen("on_ready")
async def readied():
    logger.info(f"Logged in as {bot.user}")
    async with aiosqlite.connect("db.sqlite3") as conn:
        await conn.execute('''DROP TABLE IF EXISTS games''')
        await conn.execute(
            '''CREATE TABLE IF NOT EXISTS games  (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                game_id INTEGER NOT NULL,
                channel INTEGER NOT NULL,
                registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                );'''
        )

bot.add_cog(Reg(bot))
bot.add_cog(Cron(bot))
bot.run(token)