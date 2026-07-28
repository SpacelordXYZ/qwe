import discord
from discord.ext import commands
import asyncio
import traceback

import config
import database


# =========================
# INTENTS
# =========================

intents = discord.Intents.all()


# =========================
# BOT SETUP
# =========================

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


database.setup()



# =========================
# LOAD COGS
# =========================

async def load_extensions():

    extensions = [
        "commands",
        "events"
    ]

    for extension in extensions:

        try:

            await bot.load_extension(extension)

            print(
                f"✅ Loaded {extension}.py"
            )

        except Exception:

            print(
                f"❌ Failed loading {extension}.py"
            )

            traceback.print_exc()



# =========================
# READY
# =========================

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


        print(
            f"✅ Synced {len(synced)} commands"
        )


    except Exception as e:

        print(
            "Slash sync failed:"
        )

        print(e)




# =========================
# START
# =========================

async def main():

    print(
        "Starting bot..."
    )


    if not config.TOKEN:

        print(
            "❌ TOKEN missing from .env"
        )

        input(
            "Press Enter to close..."
        )

        return



    async with bot:

        await load_extensions()


        print(
            "Connecting to Discord..."
        )


        await bot.start(
            config.TOKEN
        )



# =========================
# RUN
# =========================

try:

    asyncio.run(
        main()
    )


except KeyboardInterrupt:

    print(
        "Bot stopped."
    )


except Exception:

    print(
        "❌ Bot crashed:"
    )

    traceback.print_exc()


    input(
        "Press Enter to close..."
    )