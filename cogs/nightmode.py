from discord.ext import commands
import json

class NightMode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = "config.json"

    def save_config(self, data):
        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=4)

    @commands.command(name="nightmode")
    @commands.is_owner()
    async def nightmode(self, ctx, mode: str):
        with open(self.config_path, "r") as f:
            config = json.load(f)

        if mode.lower() == "on":
            config["nightmode"] = True
            self.save_config(config)
            await ctx.send("🌙 Night Mode is now **enabled**: All activities locked except for Owner/Admins.")
        elif mode.lower() == "off":
            config["nightmode"] = False
            self.save_config(config)
            await ctx.send("🌞 Night Mode is now **disabled**: Normal operations restored.")
        else:
            await ctx.send("⚠️ Invalid argument! Use `?nightmode on` or `?nightmode off`.")

async def setup(bot):
    await bot.add_cog(NightMode(bot))
