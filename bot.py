import discord
from discord.ext import commands
import json, os
from dotenv import load_dotenv

# Load .env (your bot token)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Load config.json
with open("config.json", "r") as f:
    config = json.load(f)

# Load or create prefixes.json
if os.path.exists("prefixes.json"):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
else:
    prefixes = {}

# Function to get prefix per guild
def get_prefix(bot, message):
    if message.guild:
        return prefixes.get(str(message.guild.id), config.get("prefix", "!"))
    return config.get("prefix", "!")  # default in DMs

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
intents.bans = True

bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.config = config
bot.prefixes = prefixes

# Ordered list of cogs
initial_cogs = [
    "cogs.antispam",
    "cogs.antiraid",
    "cogs.antilink",
    "cogs.auditlog",
    "cogs.antinuke",
    "cogs.moderation"
]

@bot.event
async def on_ready():
    try:
        if bot.user.name != "META SONIC":
            await bot.user.edit(username="META SONIC")
    except Exception as e:
        print(f"Could not rename bot automatically: {e}")

    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game("META SONIC Security Mode"))

# Save prefixes.json
def save_prefixes():
    with open("prefixes.json", "w") as f:
        json.dump(bot.prefixes, f, indent=4)

# Command to set prefix (Admin only)
@bot.command(name="setprefix")
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new_prefix: str):
    bot.prefixes[str(ctx.guild.id)] = new_prefix
    save_prefixes()
    await ctx.send(f"✅ Prefix updated to `{new_prefix}` for this server.")

@setprefix.error
async def setprefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need **Administrator** permission to change prefix.")

# Load cogs
for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        print(f"✅ Loaded {cog}")
    except Exception as e:
        print(f"❌ Failed to load {cog}: {e}")

bot.run(TOKEN)
