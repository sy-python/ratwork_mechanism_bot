import asyncio
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
        self.role_set = set(self.menace_emote_id_role_map.values())
        logger.info("Menace emote role map: %s", self.menace_emote_id_role_map)

    @discord.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
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
            if role in author.roles:
                logger.info(
                    "user %s already has %s role, skipping",
                    author.name,
                    role.name,
                )
                return
            try:
                await author.add_roles(role)
                logger.info(
                    "user %s got %s reacts with %s emoji, added role %s",
                    author.name,
                    amount,
                    payload.emoji.name,
                    role.name,
                )
            except discord.Forbidden:
                logger.info(
                    "couldn't give %s role to %s, check permissions",
                    role.name,
                    author.name,
                )

    @discord.slash_command(
        name="cleanse",
        description="Free yourself from the menace areas",
        guild_ids=[config.main_server_id],
    )
    async def cleanse(self, ctx: discord.ApplicationContext) -> None:
        if not isinstance(ctx.author, discord.Member):
            return  # This should never happen, because this command only works in the main guild
        loop = asyncio.get_running_loop()
        try:
            cleanse_cd = await loop.run_in_executor(None, check_cleanse, ctx)
        except Exception as e:
            await ctx.respond("Error occurred. Please try again later.", ephemeral=True)
            raise
        if cleanse_cd:
            await ctx.respond(
                f"Time the Healer cannot be called more often than once per week. Try again {cleanse_cd}",
                ephemeral=True,
            )
        else:
            try:
                roles_to_remove = [
                    role for role in ctx.author.roles if role in self.role_set
                ]
                if not roles_to_remove:
                    await ctx.respond(
                        "You are not in the menace areas.", ephemeral=True
                    )
                    return
                await ctx.author.remove_roles(*roles_to_remove)
                logger.info("user %s cleansed", ctx.author.name)
                await ctx.respond(
                    "Memory fades; pain departs; rewards arrive!", ephemeral=True
                )
            except discord.Forbidden:
                logger.info(
                    "couldn't remove menace roles from %s, check permissions",
                    ctx.author.name,
                )


def check_cleanse(ctx: discord.ApplicationContext) -> str:
    now = discord.utils.utcnow().timestamp()
    try:
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
                    logger.info(
                        "user %s tried to cleanse too soon, %s seconds left",
                        ctx.author.name,
                        allowed_time - now,
                    )
                    return allowed_time_string
            curr.execute(queries.update_reset, (ctx.author.id, now))
        return ""
    except Exception as e:
        logger.error("Database error: %s", e)
        raise
