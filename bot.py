import discord
from discord.ext import commands
import json
import os
import asyncio

# ----------------------------
# Load config.json
# ----------------------------
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config.get("token")
PREFIX = config.get("prefix", "?")
intents = discord.Intents.all()

# ----------------------------
# Initialize bot
# ----------------------------
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.config = config  # store config so cogs can access

# ----------------------------
# Auto load cogs
# ----------------------------
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded cog: {filename}")
            except Exception as e:
                print(f"❌ Failed to load cog {filename}: {e}")

# ----------------------------
# Events
# ----------------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name=f"Prefix: {PREFIX}"))

# ----------------------------
# Run bot
# ----------------------------
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
