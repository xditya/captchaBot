# (c) 2022 @xditya.
# Powered by apis.xditya.me

from . import bot, events


@bot.on(
    events.NewMessage(
        incoming=True, func=lambda e: not e.is_private, pattern="^/setwelcome"
    )
)
async def setwel(event):
    await event.reply("To be added soon, stay tuned - @BotzHub")
    return
