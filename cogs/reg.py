import asyncio
import aiosqlite
import logging
from disnake import Client
from disnake.ext import commands


logger = logging.getLogger("bot")

class Reg(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot
    
    @commands.slash_command(description="Register a new game to monitor")
    async def register(self, inter, title: str) -> None:
        async with aiosqlite.connect("db.sqlite3") as conn:
            data = (0, inter.channel_id)
            await conn.execute(
                "INSERT INTO games (game_id, channel) VALUES (?, ?)", 
                data,
            )
            await conn.commit()
            logger.info(f"Added {data}")
        await inter.response.send_message(f"Registered {title} for tracking")


    @commands.slash_command(description="Deregister a game")
    async def deregister(self, inter, id: int) -> None:
        async with aiosqlite.connect("db.sqlite3") as conn:
            data = (id, inter.channel_id)
            await conn.execute(
                "DELETE FROM games WHERE game_id=(?) AND channel=(?)",
                data
            )
            await conn.commit()
            logger.info(f"Removed {data}")
        await inter.response.send_message(f"Removed {id} from tracking")
