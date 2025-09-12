import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Kick command
    @commands.command(name="kick")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} has been kicked. Reason: {reason}")

    # Ban command
    @commands.command(name="ban")
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} has been banned. Reason: {reason}")

    # Unban command
    @commands.command(name="unban")
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"✅ Unbanned {user.mention}")
                return

    # Mute (role-based mute)
    @commands.command(name="mute")
    @has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f"🔇 {member.mention} has been muted. Reason: {reason}")

    # Unmute
    @commands.command(name="unmute")
    @has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"🔊 {member.mention} has been unmuted.")

    # Clear messages
    @commands.command(name="clear")
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Cleared {amount} messages.", delete_after=5)

    # Error handling
    @kick.error
    @ban.error
    @unban.error
    @mute.error
    @unmute.error
    @clear.error
    async def mod_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("❌ You don’t have permission to use this command.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
