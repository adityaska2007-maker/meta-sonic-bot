import asyncio
import os
import json

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load .env (tokens & API keys)
load_dotenv()

# Load config.json (prefix & settings)
with open("config.json", "r") as f:
    config = json.load(f)

# Tokens & API keys
TOKEN = os.getenv("TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not TOKEN:
    raise ValueError("❌ No Discord token found! Add it to .env as TOKEN=...")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    print("⚠️ Spotify credentials missing — music commands may not work.")

if not YOUTUBE_API_KEY:
    print("⚠️ YouTube API key missing — YouTube features may not work.")

PREFIX = config.get("default_prefix", "?")
intents = discord.Intents.all()

# Bot setup
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.config = config
bot.spotify_id = SPOTIFY_CLIENT_ID
bot.spotify_secret = SPOTIFY_CLIENT_SECRET
bot.youtube_key = YOUTUBE_API_KEY


async def load_cogs():
    """Auto-load all cogs in ./cogs/"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded cog: {filename}")
            except Exception as e:
                print(f"❌ Failed to load cog {filename}: {e}")


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name=f"Prefix: {PREFIX}"))


async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Fatal error: {e}")
