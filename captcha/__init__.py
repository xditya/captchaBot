# (c) 2022 @xditya.
# Powered by apis.xditya.me

import logging

import redis
from decouple import config, UndefinedValueError
from telethon import TelegramClient


logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)

log = logging.getLogger("captchaBot")

log.info("Loading config...")
try:
    BOT_TOKEN = config("BOT_TOKEN")
    REDIS_URL = config("REDIS_URL")
    REDIS_PASSWORD = config("REDIS_PASSWORD")
    AUTH = [int(i) for i in config("AUTH").split(" ")]
except UndefinedValueError as ex:
    log.exception(ex)
    exit(0)

log.info("Starting client...")
try:
    bot = TelegramClient(None, 6, "eb06d4abfb49dc3eeb1aeb98ae0f581e").start(
        bot_token=BOT_TOKEN
    )
except Exception as e:
    log.warning(e)
    exit(1)

REDIS_URL = REDIS_URL.split(":")
log.info("Getting Connection With Redis Database")
db = redis.Redis(
    host=REDIS_URL[0],
    port=REDIS_URL[1],
    password=REDIS_PASSWORD,
    decode_responses=True,
)

if db.get("CACHE") is None:
    db.set("CACHE", "{}")


async def whoami():
    me = await bot.get_me()
    log.info(
        "\n\nBot has Started.\n\nUserName: @{}\nID: {}\n\n     ~ @BotzHub".format(
            me.username, me.id
        )
    )
