import discord


class AbstractRatworkCog(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
