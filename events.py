import discord
from discord.ext import commands

import config
import logger


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ignored(self, channel):
        if not channel:
            return False
        return channel.name == config.MODLOG_CHANNEL or channel.name in config.IGNORED_CHANNELS

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        if not message.guild:
            return

        if await self.ignored(message.channel):
            return

        if config.LOG_MESSAGE_DELETE:
            await logger.message_delete(message)

    # member role update
    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        if before.roles == after.roles:
            return

        added = [
            role for role in after.roles
            if role not in before.roles
        ]

        removed = [
            role for role in before.roles
            if role not in after.roles
        ]

        for role in added:
            await logger.send_log(
                after.guild,
                "🎭 Role Added",
                (
                    f"**User:** {after.mention}\n"
                    f"**Role:** {role.mention}"
                ),
                0x00ff99
            )

        for role in removed:
            await logger.send_log(
                after.guild,
                "🎭 Role Removed",
                (
                    f"**User:** {after.mention}\n"
                    f"**Role:** {role.mention}"
                ),
                0xff9900
            )


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if not before.guild:
            return

        if await self.ignored(before.channel):
            return

        if before.content == after.content:
            return

        if config.LOG_MESSAGE_EDIT:
            await logger.message_edit(
                before,
                after
            )


    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):

        if not messages:
            return

        channel = messages[0].channel

        if await self.ignored(channel):
            return

        if config.LOG_BULK_DELETE:
            await logger.send_log(
                messages[0].guild,
                "🗑️ Bulk Message Delete",
                f"{len(messages)} messages deleted in {channel.mention}"
            )


    @commands.Cog.listener()
    async def on_member_join(self, member):

        if config.LOG_MEMBER_JOIN:
            await logger.member_join(member)


    @commands.Cog.listener()
    async def on_member_remove(self, member):

        if config.LOG_MEMBER_LEAVE:
            await logger.member_leave(member)


    @commands.Cog.listener()
    async def on_guild_role_create(self, role):

        if config.LOG_ROLE_CREATE:
            await logger.send_log(
                role.guild,
                "🎭 Role Created",
                f"Role: `{role.name}`"
            )


    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):

        if config.LOG_ROLE_DELETE:
            await logger.send_log(
                role.guild,
                "🗑️ Role Deleted",
                f"Role: `{role.name}`"
            )


    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):

        if config.LOG_ROLE_UPDATE:
            await logger.role_update(
                before,
                after
            )


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):

        if config.LOG_CHANNEL_CREATE:
            await logger.send_log(
                channel.guild,
                "📢 Channel Created",
                f"{channel.mention}"
            )


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):

        if config.LOG_CHANNEL_DELETE:
            await logger.send_log(
                channel.guild,
                "🗑️ Channel Deleted",
                f"`{channel.name}`"
            )


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):

        if config.LOG_CHANNEL_UPDATE:
            await logger.channel_update(
                before,
                after
            )


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if config.LOG_VOICE:
            await logger.voice_update(
                member,
                before,
                after
            )


async def setup(bot):
    await bot.add_cog(Events(bot))