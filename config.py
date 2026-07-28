import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# BOT TOKEN
# =========================

TOKEN = os.getenv("TOKEN")


# =========================
# MOD LOG SETTINGS
# =========================

# Channel where all logs are sent
MODLOG_CHANNEL = "mod-logs"


# =========================
# ENABLE / DISABLE LOG TYPES
# =========================

# Messages
LOG_MESSAGE_DELETE = True
LOG_MESSAGE_EDIT = True
LOG_BULK_DELETE = True


# Members
LOG_MEMBER_JOIN = True
LOG_MEMBER_LEAVE = True
LOG_MEMBER_UPDATE = True


# Roles
LOG_ROLE_CREATE = True
LOG_ROLE_DELETE = True
LOG_ROLE_UPDATE = True


# Channels
LOG_CHANNEL_CREATE = True
LOG_CHANNEL_DELETE = True
LOG_CHANNEL_UPDATE = True


# Voice
LOG_VOICE = True


# Moderation Commands
LOG_MOD_ACTIONS = True


# =========================
# IGNORED CHANNELS
# =========================

# Logs will not be sent for these channels
IGNORED_CHANNELS = [
    "bot-commands"
]


# =========================
# EMBED SETTINGS
# =========================

LOG_COLOR = 0xFF0000


# =========================
# SLASH COMMAND SETTINGS
# =========================

# Put your server ID here for instant slash command updates.
# Example:
# TEST_GUILD_ID = 123456789012345678
#
# Leave as 0 for global commands.

TEST_GUILD_ID = 1401709386262511636



# =========================
# BOT PRESENCE
# =========================

STATUS_TYPE = "watching"

STATUS_TEXT = "over the server"



# =========================
# DATABASE SETTINGS
# =========================

DATABASE_FILE = "moderation.db"



# =========================
# PERMISSION SETTINGS
# =========================

# Roles allowed to use owner-level commands
OWNER_ROLES = [
    "Owner",
    "Administrator"
]


# =========================
# AUTOMOD SETTINGS
# =========================

# Future automod options

ANTI_SPAM = True
ANTI_LINKS = False
ANTI_MENTION_SPAM = True