import sqlite3
import logging
from disnake import Client
from disnake.ext import commands


logger = logging.getLogger("bot")

class Reg(commands.Cog):
    def __init__(self, bot: Client, db: sqlite3.Connection):
        self.bot = bot
        self.db = db
        self.cursor = self.db.cursor()
    
    @commands.slash_command(description="Register a new game to monitor")
    async def register(self, inter, title: str) -> None:
        with self.db:
            data = (0, inter.channel_id)
            self.cursor.execute(
                "INSERT INTO games (game_id, channel) VALUES (?, ?)", 
                data,
            )
            logger.info(f"Added {data}")
        await inter.response.send_message(f"Registered {title} for tracking")


    @commands.slash_command(description="Deregister a game")
    async def deregister(self, inter, id: int) -> None:
        with self.db:
            data = (id, inter.channel_id)
            self.cursor.execute(
                "DELETE FROM games WHERE game_id=(?) AND channel=(?)",
                data
            )
            logger.info(f"Removed {data}")
        await inter.response.send_message(f"Removed {id} from tracking")
