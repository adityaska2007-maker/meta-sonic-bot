from discord.ext import commands
import json

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setprefix")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, new_prefix):
        self.bot.config['default_prefix'] = new_prefix
        with open('config.json', 'w') as f:
            json.dump(self.bot.config, f, indent=4)

        await ctx.send(f"✅ Prefix has been changed to: `{new_prefix}`")
        await self.bot.change_presence(activity=discord.Game(name=f"Prefix: {new_prefix}"))

def setup(bot):
    bot.add_cog(Prefix(bot))
