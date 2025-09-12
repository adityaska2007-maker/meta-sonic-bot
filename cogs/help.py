import discord
from discord.ext import commands
from discord.ui import View, Button

class HelpView(View):
    def __init__(self, prefix):
        super().__init__(timeout=None)
        self.prefix = prefix

        # Add buttons
        self.add_item(Button(label="Main Module", style=discord.ButtonStyle.primary, custom_id="main"))
        self.add_item(Button(label="Extra Module", style=discord.ButtonStyle.primary, custom_id="extra"))
        self.add_item(Button(label="Search Command", style=discord.ButtonStyle.secondary, custom_id="search"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Allow only the user who ran help to click
        return True

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    async def on_error(self, interaction: discord.Interaction, error: Exception, item):
        await interaction.response.send_message("⚠️ Something went wrong.", ephemeral=True)

    @discord.ui.button(label="Main Module", style=discord.ButtonStyle.primary, custom_id="main_btn")
    async def main_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="📖 META SONIC - Main Modules",
            description=f"Prefix: `{self.prefix}`\nUse `{self.prefix}help <command>` for details.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="🔹 Main Modules",
            value=(
                "🛡️ AntiNuke\n"
                "🔗 AntiLink\n"
                "👥 AntiRaid\n"
                "💬 AntiSpam\n"
                "📝 Audit Log\n"
                "🔨 Moderation\n"
                "⚙️ Utility"
            ),
            inline=False
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Extra Module", style=discord.ButtonStyle.primary, custom_id="extra_btn")
    async def extra_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="📖 META SONIC - Extra Modules",
            description=f"Prefix: `{self.prefix}`\nExtra features coming soon.",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="🔹 Extra",
            value="🤖 Auto Responder\n🎭 Custom Roles\n📝 Logging\n🎙️ VCRoles\n⭐ Fun\n📦 Bot",
            inline=False
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Search Command", style=discord.ButtonStyle.secondary, custom_id="search_btn")
    async def search_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="🔍 META SONIC - Command Search",
            description=f"Use `{self.prefix}help <command>` to see details about a command.\n\nExample:\n`{self.prefix}help ban`",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        prefix = self.bot.config.get("prefix", "?")

        embed = discord.Embed(
            title="📖 META SONIC Help Menu",
            description=f"**Prefix is `{prefix}`**\nUse `{prefix}help <command | module>` for more info.",
            color=discord.Color.blue()
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url="https://i.ibb.co/vwZt2mR/meta-sonic.png")  # bot logo

        embed.add_field(
            name="🔹 Main Modules",
            value=(
                "🛡️ AntiNuke\n"
                "🔗 AntiLink\n"
                "👥 AntiRaid\n"
                "💬 AntiSpam\n"
                "📝 Audit Log\n"
                "🔨 Moderation\n"
                "⚙️ Utility"
            ),
            inline=False
        )

        embed.set_footer(text="Powered by META SONIC HQ")

        view = HelpView(prefix)
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
