import datetime

import discord

from .base import AbstractRatworkCog
from ..config import config, logger, queries, BotSetupError

WEEK = 60 * 60 * 24 * 7


class MenaceCog(AbstractRatworkCog):
    @discord.Cog.listener(once=True)
    async def on_ready(self):
        self.main_server: discord.Guild = await discord.utils.get_or_fetch(
            self.bot,
            "guild",
            config.main_server_id,
        )
        logger.info("Main server: %s", self.main_server.name)
        role_ids = set(config.menace_emote_role_map.values())
        roles: dict[int, discord.Role] = {}
        for role in self.main_server.roles:
            if role.id in role_ids:
                roles[role.id] = role
                role_ids.remove(role.id)
        if role_ids:
            raise BotSetupError(f"Missing roles: {', '.join(map(str, role_ids))}")
        self.menace_emote_id_role_map = {
            emoji_id: roles[role_id]
            for emoji_id, role_id in config.menace_emote_role_map.items()
        }
        logger.info("Menace emote role map: %s", self.menace_emote_id_role_map)

    @discord.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        logger.info(payload)
        if payload.emoji.id not in self.menace_emote_id_role_map:
            return
        if payload.guild_id != self.main_server.id:
            return
        channel: discord.abc.PartialMessageableChannel = (
            await discord.utils.get_or_fetch(
                self.main_server,
                "channel",
                payload.channel_id,
            )
        )
        message = await channel.fetch_message(payload.message_id)
        logger.info(message.author)
        logger.info(type(message.author))
        if not isinstance(message.author, discord.Member):
            author: discord.Member = await discord.utils.get_or_fetch(
                self.main_server,
                "member",
                message.author.id,
            )
        else:
            author = message.author
        amount = 0
        for reaction in message.reactions:
            if isinstance(reaction.emoji, str):
                continue
            if reaction.emoji.id == payload.emoji.id:
                amount = reaction.count
        if amount == config.menace_threshold:
            role = self.menace_emote_id_role_map[payload.emoji.id]
            await author.add_roles(role)
            logger.info(
                "user %s got %s reacts with %s emoji, added role %s",
                author.name,
                amount,
                payload.emoji.name,
                role.name,
            )

    @discord.slash_command(
        name="cleanse",
        description="Free yourself from the menace areas",
        guild_ids=[config.main_server_id],
    )
    async def cleanse(self, ctx: discord.ApplicationContext) -> None:
        if not isinstance(ctx.author, discord.Member):
            return  # This should never happen, because this command only works in the main guild
        now = discord.utils.utcnow().timestamp()
        with config.connection as conn:
            curr = conn.cursor()
            curr.execute(queries.get_reset, (ctx.author.id,))
            row = curr.fetchone()
            if row is not None:
                allowed_time = row[0] + WEEK
                if now < allowed_time:
                    allowed_time_object = datetime.datetime.fromtimestamp(
                        allowed_time, tz=datetime.timezone.utc
                    )
                    allowed_time_string = discord.utils.format_dt(
                        allowed_time_object, style="R"
                    )
                    await ctx.respond(
                        f"Time the Healer cannot be called more often than once per week. Try again {allowed_time_string}",
                        ephemeral=True,
                    )
                    logger.info(
                        "user %s tried to cleanse too soon, %s seconds left",
                        ctx.author.name,
                        allowed_time - now,
                    )
                    return
            curr.execute(queries.update_reset, (ctx.author.id, now))
        await ctx.author.remove_roles(*self.menace_emote_id_role_map.values())
        await ctx.respond("Memory fades; pain departs; rewards arrive!", ephemeral=True)
        logger.info("user %s cleansed", ctx.author.name)
