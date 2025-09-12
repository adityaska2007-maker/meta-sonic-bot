import discord
from discord.ext import commands

class AuditLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_log_channel(self, guild):
        log_channel_id = self.bot.config.get("log_channel_id")
        if log_channel_id:
            return guild.get_channel(int(log_channel_id))
        return None

    # --- MEMBER EVENTS ---
    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = self.get_log_channel(member.guild)
        if log_channel:
            await log_channel.send(f"✅ **Member Joined:** {member.mention} ({member.id})")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = self.get_log_channel(member.guild)
        if log_channel:
            await log_channel.send(f"❌ **Member Left/Kicked:** {member.mention} ({member.id})")

    # --- MESSAGE EVENTS ---
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return
        log_channel = self.get_log_channel(message.guild)
        if log_channel:
            await log_channel.send(
                f"🗑️ **Message deleted** in {message.channel.mention} by {message.author.mention}\n"
                f"Content: `{message.content}`"
            )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or not before.guild:
            return
        if before.content == after.content:
            return
        log_channel = self.get_log_channel(before.guild)
        if log_channel:
            await log_channel.send(
                f"✏️ **Message edited** in {before.channel.mention} by {before.author.mention}\n"
                f"Before: `{before.content}`\nAfter: `{after.content}`"
            )

    # --- ROLE UPDATES ---
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        log_channel = self.get_log_channel(role.guild)
        if log_channel:
            await log_channel.send(f"➕ **Role Created:** {role.name}")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        log_channel = self.get_log_channel(role.guild)
        if log_channel:
            await log_channel.send(f"➖ **Role Deleted:** {role.name}")

    # --- CHANNEL UPDATES ---
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = self.get_log_channel(channel.guild)
        if log_channel:
            await log_channel.send(f"📢 **Channel Created:** {channel.name}")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = self.get_log_channel(channel.guild)
        if log_channel:
            await log_channel.send(f"📉 **Channel Deleted:** {channel.name}")

async def setup(bot):
    await bot.add_cog(AuditLog(bot))
