import logging
import os
import sys

import telegram.ext as tg

print("haruka")
print("Starting...")


# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
#if sys.version_info[0] < 3 or sys.version_info[1] < 6:
#    LOGGER.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
#``````````````    quit(1)

ENV = bool(os.environ.get('ENV', True))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)
    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    MESSAGE_DUMP = os.environ.get('MESSAGE_DUMP', None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
    except ValueError:
        raise Exception("Your sudo users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(int(x) for x in os.environ.get("SUPPORT_USERS", "").split())
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(int(x) for x in os.environ.get("WHITELIST_USERS", "").split())
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    URL = os.environ.get('URL', "")  # Does not contain token
    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    OPENWEATHERMAP_ID = os.environ.get('OPENWEATHERMAP_ID', None)
    GENIUS_API = os.environ.get('GENIUS_API', None)
    DB_URI = os.environ.get('DATABASE_URL')
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
    STRICT_ANTISPAM = bool(os.environ.get('STRICT_ANTISPAM', False))
    DEEPFRY_TOKEN = os.environ.get('DEEPFRY_TOKEN', "")
    LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)
    WORKERS = int(os.environ.get('WORKERS', 8))
    BAN_STICKER = os.environ.get('BAN_STICKER', 'CAADAgADEAgAAgi3GQL9YQyT_kBpQwI')
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False)
    SUDO_USERS.add(OWNER_ID)
    updater = tg.Updater(TOKEN, workers=WORKERS)
    dispatcher = updater.dispatcher
    SUDO_USERS = list(SUDO_USERS)
    WHITELIST_USERS = list(WHITELIST_USERS)
    IBM_WATSON_CRED_URL = os.environ.get('IBM_WATSON_CRED_URL', None)
    IBM_WATSON_CRED_PASSWORD = os.environ.get('IBM_WATSON_CRED_PASSWORD', None)
    SUPPORT_USERS = list(SUPPORT_USERS)
    # Load at end to ensure all prev variables have been set
    from haruka.modules.helper_funcs.handlers import CustomCommandHandler, CustomRegexHandler, GbanLockHandler
    # make sure the regex handler can take extra kwargs
    tg.RegexHandler = CustomRegexHandler
    if ALLOW_EXCL:
       tg.CommandHandler = CustomCommandHandler
    tg.CommandHandler = GbanLockHandler

else:
   quit(1)

