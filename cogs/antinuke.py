import discord
from discord.ext import commands

class AntiNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_trusted(self, user_id: int):
        return str(user_id) in self.bot.config.get("trusted_users", [])

    async def punish(self, guild, user, action: str):
        log_channel = self.bot.get_channel(int(self.bot.config["log_channel_id"]))
        member = guild.get_member(user.id)

        if log_channel:
            await log_channel.send(f"🚨 **AntiNuke triggered**: {user.mention} attempted {action}!")

        if member and not self.is_trusted(user.id):
            try:
                await member.kick(reason=f"AntiNuke: unauthorized {action}")
                if log_channel:
                    await log_channel.send(f"🦵 {member.mention} kicked for **{action}**")
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            await self.punish(guild, entry.user, "channel delete")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = role.guild
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            await self.punish(guild, entry.user, "role delete")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            await self.punish(guild, entry.user, "ban")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            await self.punish(guild, entry.user, "kick")

    @commands.command(name="antinuke")
    @commands.has_permissions(administrator=True)
    async def toggle_antinuke(self, ctx, mode: str = None):
        """
        Enable/disable AntiNuke
        Usage: !ms antinuke on / off
        """
        if mode not in ["on", "off"]:
            return await ctx.send("Usage: `antinuke on` or `antinuke off`")

        self.bot.config["antinuke"] = (mode == "on")
        await ctx.send(f"✅ AntiNuke is now **{mode.upper()}**")

async def setup(bot):
    await bot.add_cog(AntiNuke(bot))
