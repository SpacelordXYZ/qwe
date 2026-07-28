import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

import database
import logger


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def can_moderate(self, interaction, user):

        if user == interaction.guild.owner:
            return False

        if user.top_role >= interaction.user.top_role:
            return False

        if user.top_role >= interaction.guild.me.top_role:
            return False

        return True


    async def deny(self, interaction):

        await interaction.response.send_message(
            "❌ You cannot moderate this user.",
            ephemeral=True
        )


    #ping
    @app_commands.command(name="ping", description="Shows bot ping")
    async def ping(self, interaction):

        await interaction.response.send_message(
            f"🏓 {round(self.bot.latency * 1000)}ms"
        )


    #userinfo
    @app_commands.command(name="userinfo", description="Shows user information")
    async def userinfo(self, interaction, user: discord.Member):

        embed = discord.Embed(
            title=f"User Info - {user}",
            color=0x00ff00
        )

        embed.set_thumbnail(
            url=user.display_avatar.url
        )

        embed.add_field(
            name="ID",
            value=user.id
        )

        embed.add_field(
            name="Joined",
            value=user.joined_at
        )

        embed.add_field(
            name="Created",
            value=user.created_at
        )

        await interaction.response.send_message(
            embed=embed
        )


    #warn
    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction, user: discord.Member, reason: str):

        if not await self.can_moderate(interaction, user):
            return await self.deny(interaction)

        warning = database.add_warning(
            user.id,
            interaction.user.id,
            reason
        )

        case = database.add_case(
            user.id,
            interaction.user.id,
            "WARN",
            reason
        )

        await logger.mod_action(
            interaction.guild,
            "⚠️ Warning",
            interaction.user,
            user,
            reason,
            case
        )

        await interaction.response.send_message(
            f"⚠️ Warned {user.mention}\nWarning ID: `{warning}`\nCase: `{case}`"
        )


    #checkwarns
    @app_commands.command(name="checkwarns", description="Check warnings")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def checkwarns(self, interaction, user: discord.Member):

        warns = database.get_warnings(user.id)

        if not warns:
            return await interaction.response.send_message(
                "No warnings found."
            )

        embed = discord.Embed(
            title=f"Warnings - {user}",
            color=0xffaa00
        )

        for warn in warns:

            embed.add_field(
                name=f"Warning #{warn[0]}",
                value=f"Reason: {warn[3]}\nDate: {warn[4]}",
                inline=False
            )

        await interaction.response.send_message(
            embed=embed
        )


    #removewarn
    @app_commands.command(name="removewarn", description="Remove warning by ID")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def removewarn(self, interaction, warning_id: int):

        database.remove_warning(
            warning_id
        )

        await interaction.response.send_message(
            f"✅ Removed warning `{warning_id}`"
        )


    #clearwarn
    @app_commands.command(name="clearwarn", description="Clear warnings")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clearwarn(self, interaction, user: discord.Member):

        if not await self.can_moderate(interaction, user):
            return await self.deny(interaction)

        database.clear_warnings(
            user.id
        )

        await interaction.response.send_message(
            f"✅ Cleared warnings for {user.mention}"
        )


    #history
    @app_commands.command(name="history", description="View moderation history")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def history(self, interaction, user: discord.Member):

        cases = database.get_history(
            user.id
        )

        if not cases:
            return await interaction.response.send_message(
                "No history found."
            )

        embed = discord.Embed(
            title=f"History - {user}",
            color=0xff0000
        )

        for case in cases[:10]:

            embed.add_field(
                name=f"Case #{case[0]} {case[3]}",
                value=f"Reason: {case[4]}\nDate: {case[5]}",
                inline=False
            )

        await interaction.response.send_message(
            embed=embed
        )

    #ban
    @app_commands.command(name="ban", description="Ban a user by ID")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction, user_id: str, reason: str):

        try:
            user = await self.bot.fetch_user(int(user_id))
        except:
            return await interaction.response.send_message(
                "❌ Invalid user ID.",
                ephemeral=True
            )

        member = interaction.guild.get_member(user.id)

        if member and not await self.can_moderate(interaction, member):
            return await self.deny(interaction)

        case = database.add_case(
            user.id,
            interaction.user.id,
            "BAN",
            reason
        )

        await interaction.guild.ban(
            user,
            reason=reason
        )

        await logger.mod_action(
            interaction.guild,
            "🔨 Ban",
            interaction.user,
            user,
            reason,
            case
        )

        await interaction.response.send_message(
            f"🔨 Banned `{user}`\nCase: `{case}`"
        )


    #unban
    @app_commands.command(name="unban", description="Unban a user by ID")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction, user_id: str):

        try:
            user = await self.bot.fetch_user(int(user_id))
        except:
            return await interaction.response.send_message(
                "❌ Invalid user ID.",
                ephemeral=True
            )

        try:
            await interaction.guild.unban(user)

        except:
            return await interaction.response.send_message(
                "❌ User is not banned.",
                ephemeral=True
            )

        case = database.add_case(
            user.id,
            interaction.user.id,
            "UNBAN",
            "No reason provided"
        )

        await logger.mod_action(
            interaction.guild,
            "🔓 Unban",
            interaction.user,
            user,
            "No reason provided",
            case
        )

        await interaction.response.send_message(
            f"🔓 Unbanned `{user}`\nCase: `{case}`"
        )


    #kick
    @app_commands.command(name="kick", description="Kick a user")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction, user: discord.Member, reason: str):

        if not await self.can_moderate(interaction, user):
            return await self.deny(interaction)

        case = database.add_case(
            user.id,
            interaction.user.id,
            "KICK",
            reason
        )

        await user.kick(
            reason=reason
        )

        await logger.mod_action(
            interaction.guild,
            "👢 Kick",
            interaction.user,
            user,
            reason,
            case
        )

        await interaction.response.send_message(
            f"👢 Kicked {user.mention}\nCase: `{case}`"
        )


    #timeout
    @app_commands.command(name="timeout", description="Timeout a user")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction, user: discord.Member, minutes: int, reason: str):

        if not await self.can_moderate(interaction, user):
            return await self.deny(interaction)

        case = database.add_case(
            user.id,
            interaction.user.id,
            "TIMEOUT",
            reason
        )

        await user.timeout(
            timedelta(minutes=minutes),
            reason=reason
        )

        await logger.mod_action(
            interaction.guild,
            "⏳ Timeout",
            interaction.user,
            user,
            reason,
            case
        )

        await interaction.response.send_message(
            f"⏳ Timed out {user.mention}\nCase: `{case}`"
        )


    #untimeout
    @app_commands.command(name="untimeout", description="Remove timeout")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout(self, interaction, user: discord.Member):

        if not await self.can_moderate(interaction, user):
            return await self.deny(interaction)

        await user.timeout(None)

        case = database.add_case(
            user.id,
            interaction.user.id,
            "UNTIMEOUT",
            "Removed timeout"
        )

        await interaction.response.send_message(
            f"✅ Removed timeout from {user.mention}\nCase: `{case}`"
        )


    #purge
    @app_commands.command(name="purge", description="Delete messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction, amount: int):

        await interaction.response.defer(
            ephemeral=True
        )

        deleted = await interaction.channel.purge(
            limit=amount
        )

        await logger.send_log(
            interaction.guild,
            "🗑️ Purge",
            f"{interaction.user.mention} deleted `{len(deleted)}` messages in {interaction.channel.mention}"
        )

        await interaction.followup.send(
            f"🗑️ Purged {len(deleted)} messages.",
            ephemeral=True
        )


    #lock
    @app_commands.command(name="lock", description="Lock channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction):

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            send_messages=False
        )

        await interaction.response.send_message(
            "🔒 Channel locked."
        )


    #unlock
    @app_commands.command(name="unlock", description="Unlock channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction):

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            send_messages=True
        )

        await interaction.response.send_message(
            "🔓 Channel unlocked."
        )


    #slowmode
    @app_commands.command(name="slowmode", description="Set slowmode")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction, seconds: int):

        await interaction.channel.edit(
            slowmode_delay=seconds
        )

        await interaction.response.send_message(
            f"🐢 Slowmode set to {seconds}s."
        )


    #role
    @app_commands.command(name="role", description="Give a role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role(self, interaction, user: discord.Member, role: discord.Role):

        if role >= interaction.user.top_role:
            return await interaction.response.send_message(
                "❌ You cannot give a role equal or higher than yours.",
                ephemeral=True
            )

        if role >= interaction.guild.me.top_role:
            return await interaction.response.send_message(
                "❌ My role is not high enough.",
                ephemeral=True
            )

        await user.add_roles(role)

        await logger.role_add(
            interaction.guild,
            interaction.user,
            user,
            role
        )

        await interaction.response.send_message(
            f"✅ Added {role.mention} to {user.mention}"
        )


    #reply
    @app_commands.command(name="reply", description="Make the bot reply")
    async def reply(self, interaction, message: str):

        await interaction.response.send_message(
            message
        )


async def setup(bot):
    await bot.add_cog(
        Moderation(bot)
    )