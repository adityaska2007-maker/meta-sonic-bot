from discord.ext import commands

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ytkey(self, ctx):
        """Check YouTube API key"""
        key = self.bot.youtube_key
        if key:
            await ctx.send("✅ YouTube API key is loaded.")
        else:
            await ctx.send("❌ No YouTube API key found.")

    @commands.command()
    async def spotifykey(self, ctx):
        """Check Spotify credentials"""
        if self.bot.spotify_id and self.bot.spotify_secret:
            await ctx.send("✅ Spotify API keys are loaded.")
        else:
            await ctx.send("❌ Spotify credentials missing.")

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
