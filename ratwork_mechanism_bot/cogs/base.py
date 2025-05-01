import discord


class AbstractRatworkCog(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
