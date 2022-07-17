import logging
import sqlite3
from disnake import Client
from disnake.ext import tasks
from disnake.ext import commands


logger = logging.getLogger("bot")

class Cron(commands.Cog):
    def __init__(self, bot: Client, db: sqlite3.Connection):
        self.index = 0
        self.bot = bot
        self.db = db
        self.cursor = self.db.cursor()
        self.check_sales.start()

    def cog_unload(self):
        self.check_sales.cancel()

    def getTimeUntilTomorrow() -> int:
        return 10

    @tasks.loop(seconds=getTimeUntilTomorrow())
    async def check_sales(self):
        for row in self.cursor.execute("SELECT game_id, channel FROM games"):
            game = row[0]
            channel_id = row[1]
            channel = await self.bot.fetch_channel(channel_id)
            if channel:
                await channel.send(game)
        self.index += 1
        logger.info(f"{self.index} seconds")