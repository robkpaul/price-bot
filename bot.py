from disnake.ext import commands
from dotenv import load_dotenv
import sqlite3, os

env = load_dotenv()
token = os.environ.get("DISCORD_TOKEN")

db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()
cursor.execute('''DROP TABLE IF EXISTS games''')
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS games  (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        game_id INTEGER NOT NULL,
        guild INTEGER NOT NULL,
        channel INTEGER NOT NULL,
        registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );'''
)

bot = commands.Bot(
    command_prefix = "!",
    sync_commands=True
)

@bot.slash_command(description="Register a new game to monitor")
async def register(inter, title: str) -> None:
    with db:
        data = (0, inter.guild_id, inter.channel_id)
        cursor.execute(
            "INSERT INTO games (game_id, guild, channel) VALUES (?, ?, ?)", 
            data,
        )
    await inter.response.send_message(f"Registered {title} for tracking")

@bot.slash_command(description="Deregister a game")
async def deregister(inter, id: int) -> None:
    with db:
        data = (id, inter.guild_id, inter.channel_id)
        cursor.execute(
            "DELETE FROM games WHERE game_id=(?) AND guild=(?) AND channel=(?)",
            data
        )
    await inter.response.send_message(f"Removed {id} from tracking")

bot.run(token)