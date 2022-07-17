from datetime import time
import logging
import aiosqlite
from timeit import default_timer as timer
from disnake import Client
from disnake.ext import tasks
from disnake.ext import commands


logger = logging.getLogger("bot")

class Cron(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot
        self.check_sales.start()
        self.run_at = time(10)

    def cog_unload(self):
        self.check_sales.cancel()

    @tasks.loop(seconds=5)
    async def check_sales(self):
        start = timer()
        async with aiosqlite.connect("db.sqlite3") as conn:
            async with conn.execute("SELECT game_id, channel FROM games") as cursor:
                async for row in cursor:
                    game = row[0]
                    channel_id = row[1]
                    channel = await self.bot.fetch_channel(channel_id)
                    if channel:
                        await channel.send(game)
        end = timer()
        logger.info(f"check_sales took {end-start}")

    @check_sales.before_loop
    async def before_check_sales(self):
        await self.bot.wait_until_ready()