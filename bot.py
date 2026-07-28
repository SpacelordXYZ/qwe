import discord
from discord.ext import commands
import asyncio
import traceback

from keep_alive import keep_alive

import config
import database


intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


database.setup()


async def load_extensions():

    extensions = [
        "commands",
        "events"
    ]

    for extension in extensions:

        try:
            await bot.load_extension(extension)
            print(f"✅ Loaded {extension}.py")

        except commands.ExtensionError:
            print(f"❌ Failed loading {extension}.py")
            traceback.print_exc()


@bot.event
async def on_ready():

    print("-------------------------")
    print(f"Logged in as {bot.user}")
    print("-------------------------")

    try:

        if config.TEST_GUILD_ID:

            guild = discord.Object(
                id=config.TEST_GUILD_ID
            )

            bot.tree.copy_global_to(
                guild=guild
            )

            synced = await bot.tree.sync(
                guild=guild
            )

        else:

            synced = await bot.tree.sync()

        print(f"✅ Synced {len(synced)} commands")

    except discord.HTTPException as error:

        print("❌ Slash sync failed:")
        print(error)


async def main():

    print("Starting bot...")

    if not config.TOKEN:

        print("❌ TOKEN missing from environment variables")
        return

    await load_extensions()

    print("Connecting to Discord...")

    await bot.start(
        config.TOKEN
    )


if __name__ == "__main__":

    try:

        keep_alive()

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print("Bot stopped.")

    except discord.LoginFailure:

        print("❌ Invalid Discord token.")

    except discord.ConnectionClosed:

        print("❌ Discord connection closed.")

    except RuntimeError as error:

        print("❌ Runtime error:")
        print(error)