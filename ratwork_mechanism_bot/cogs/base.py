import discord


class AbstractRatworkCog(discord.Cog):
    def __init__(self, bot):
        """
        Initializes the cog with a reference to the Discord bot instance.
        
        Args:
        	bot: The Discord bot instance to associate with this cog.
        """
        self.bot = bot
