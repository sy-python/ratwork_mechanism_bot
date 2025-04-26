import discord


class AbstractRatworkCog(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    def __init_subclass__(cls) -> None:
        cogs.append(cls)
        return super().__init_subclass__()


cogs: list[type[AbstractRatworkCog]] = []
