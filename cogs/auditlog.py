import discord
from discord.ext import commands
import json

class AuditLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_path = "config.json"

    def get_log_channel(self, guild):
        log_channel_id = self.bot.config.get("log_channel_id")
        if log_channel_id:
            return guild.get_channel(int(log_channel_id))
        return None

    def is_nightmode_enabled(self):
        with open(self.config_path, "r") as f:
            config = json.load(f)
        return config.get("nightmode", False)

    async def log_to_channel(self, guild, message):
        log_channel = self.get_log_channel(guild)
        if log_channel:
            await log_channel.send(message)

    # --- MEMBER EVENTS ---
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.is_nightmode_enabled() and member.id != self.bot.owner_id:
            await self.log_to_channel(member.guild, f"⚠️ Blocked Member Join during Night Mode: {member} ({member.id})")
            return  # You could kick the member or log only

        await self.log_to_channel(member.guild, f"✅ **Member Joined:** {member.mention} ({member.id})")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.log_to_channel(member.guild, f"❌ **Member Left/Kicked:** {member.mention} ({member.id})")

    # --- MESSAGE EVENTS ---
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return
        await self.log_to_channel(message.guild, f"🗑️ **Message deleted** in {message.channel.mention} by {message.author.mention}\nContent: `{message.content}`")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or not before.guild:
            return
        if before.content == after.content:
            return
        await self.log_to_channel(before.guild, f"✏️ **Message edited** in {before.channel.mention} by {before.author.mention}\nBefore: `{before.content}`\nAfter: `{after.content}`")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await self.log_to_channel(role.guild, f"➕ **Role Created:** {role.name}")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await self.log_to_channel(role.guild, f"➖ **Role Deleted:** {role.name}")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if self.is_nightmode_enabled():
            await channel.delete()
            await self.log_to_channel(channel.guild, f"⚠️ **Blocked Channel Creation** during Night Mode: `{channel.name}`")
            return
        await self.log_to_channel(channel.guild, f"📢 **Channel Created:** {channel.name}")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await self.log_to_channel(channel.guild, f"📉 **Channel Deleted:** {channel.name}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        if self.is_nightmode_enabled() and message.author.id != self.bot.owner_id:
            await message.delete()
            await self.log_to_channel(message.guild, f"⚠️ **Blocked Message Send** during Night Mode by `{message.author}` in {message.channel.mention}: `{message.content}`")
            try:
                await message.author.send("⚠️ Night Mode is active: Actions are restricted.")
            except:
                pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if self.is_nightmode_enabled() and member.id != self.bot.owner_id:
            if not before.channel and after.channel:
                await member.move_to(None)  # Force disconnect
                await self.log_to_channel(member.guild, f"⚠️ **Blocked VC Join** during Night Mode by `{member}` in `{after.channel.name}`")

async def setup(bot):
    await bot.add_cog(AuditLog(bot))
