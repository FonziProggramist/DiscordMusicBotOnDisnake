import disnake
from disnake.ext import commands
import os

from settings import config

client = commands.Bot(command_prefix="!", intents=disnake.Intents.all())
client.remove_command("help")

@client.event
async def on_ready():
    print(f"В сети с ником {client.user.name}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(config['TOKEN'])