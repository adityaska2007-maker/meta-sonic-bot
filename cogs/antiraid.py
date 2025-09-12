import discord
from discord.ext import commands
import asyncio
import time
from collections import defaultdict

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.join_history = defaultdict(list)  # {guild_id: [timestamps]}

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not member.guild:
            return

        cfg = self.bot.config.get("raid", {"window": 10, "max_joins": 4})
        window = cfg.get("window", 10)     # seconds
        max_joins = cfg.get("max_joins", 4)

        guild_id = member.guild.id
        now = time.time()

        # Clean old joins
        self.join_history[guild_id] = [
            t for t in self.join_history[guild_id] if now - t <= window
        ]
        self.join_history[guild_id].append(now)

        if len(self.join_history[guild_id]) > max_joins:
            # Possible raid detected
            log_channel = self.bot.get_channel(int(self.bot.config["log_channel_id"]))
            if log_channel:
                await log_channel.send(
                    f"🚨 **AntiRaid triggered in {member.guild.name}**!\n"
                    f"Too many joins ({len(self.join_history[guild_id])}) within {window}s."
                )

            try:
                await member.guild.edit(verification_level=discord.VerificationLevel.high)
                if log_channel:
                    await log_channel.send("🔒 Server verification level raised to **HIGH** temporarily.")
            except Exception as e:
                print(f"[AntiRaid] Failed to raise verification level: {e}")

            # Optional: Kick last joiner
            try:
                await member.kick(reason="AntiRaid: mass join detected")
                if log_channel:
                    await log_channel.send(f"🦵 {member.mention} was kicked as part of AntiRaid protection.")
            except:
                pass

    @commands.command(name="antiraid")
    @commands.has_permissions(administrator=True)
    async def toggle_antiraid(self, ctx, mode: str = None):
        """
        Enable/disable AntiRaid per guild
        Usage: !ms antiraid on / off
        """
        if mode not in ["on", "off"]:
            return await ctx.send("Usage: `antiraid on` or `antiraid off`")

        self.bot.config["antiraid"] = (mode == "on")
        await ctx.send(f"✅ AntiRaid is now **{mode.upper()}**")

async def setup(bot):
    await bot.add_cog(AntiRaid(bot))
