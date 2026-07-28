import discord
import config


async def get_log_channel(guild):

    if not guild:
        return None

    return discord.utils.get(
        guild.text_channels,
        name=config.MODLOG_CHANNEL
    )


async def send_log(guild, title, description, color=0xff0000):

    channel = await get_log_channel(guild)

    if not channel:
        print("Mod log channel not found")
        return

    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=discord.utils.utcnow()
    )

    await channel.send(embed=embed)


async def mod_action(guild, action, moderator, user, reason, case=None):

    text = (
        f"**User:** {user.mention if hasattr(user,'mention') else user}\n"
        f"**User ID:** `{user.id}`\n"
        f"**Moderator:** {moderator.mention}\n"
        f"**Reason:** {reason}"
    )

    if case:
        text += f"\n**Case:** `#{case}`"

    await send_log(
        guild,
        action,
        text
    )


async def role_add(guild, moderator, user, role):

    await send_log(
        guild,
        "🎭 Role Added",
        (
            f"**User:** {user.mention}\n"
            f"**Moderator:** {moderator.mention}\n"
            f"**Role:** {role.mention}"
        ),
        0x0099ff
    )


async def role_remove(guild, moderator, user, role):

    await send_log(
        guild,
        "🎭 Role Removed",
        (
            f"**User:** {user.mention}\n"
            f"**Moderator:** {moderator.mention}\n"
            f"**Role:** {role.mention}"
        ),
        0xff9900
    )


async def message_delete(message):

    await send_log(
        message.guild,
        "🗑️ Message Deleted",
        (
            f"**Author:** {message.author.mention}\n"
            f"**Channel:** {message.channel.mention}\n\n"
            f"{message.content or '[No content]'}"
        ),
        0xff9900
    )


async def message_edit(before, after):

    await send_log(
        before.guild,
        "✏️ Message Edited",
        (
            f"**User:** {before.author.mention}\n"
            f"**Channel:** {before.channel.mention}\n\n"
            f"Before:\n{before.content}\n\n"
            f"After:\n{after.content}"
        ),
        0xffff00
    )


async def member_join(member):

    await send_log(
        member.guild,
        "📥 Member Joined",
        f"{member.mention} joined.",
        0x00ff00
    )


async def member_leave(member):

    await send_log(
        member.guild,
        "📤 Member Left",
        f"{member} left.",
        0xff0000
    )


async def role_update(before, after):

    await send_log(
        before.guild,
        "🎭 Role Updated",
        f"{before.name} → {after.name}",
        0x0099ff
    )


async def channel_update(before, after):

    await send_log(
        before.guild,
        "📢 Channel Updated",
        f"{before.name} → {after.name}",
        0x0099ff
    )


async def voice_update(member, before, after):

    await send_log(
        member.guild,
        "🔊 Voice Update",
        f"{member.mention} changed voice state.",
        0x9900ff
    )