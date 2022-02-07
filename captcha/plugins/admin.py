from . import events, bot
from .database_fns import get_all
from .. import AUTH


@bot.on(events.NewMessage(incoming=True, from_users=AUTH, pattern="^/stats$"))
async def auth_(event):
    await event.reply(
        "**Bot stats**\n\nUsers: {}\nGroups added: {}".format(
            len(get_all("users")), len(get_all("group"))
        )
    )


@bot.on(events.NewMessage(incoming=True, from_users=AUTH, pattern="^/broadcast ?(.*)"))
async def broad(e):
    msg = e.pattern_match.group(1)
    if not msg:
        return await e.reply("Please use `/broadcast a_message_here`")
    xx = await e.reply("In progress...")
    users = get_all("users")
    done = error = 0
    for i in users:
        try:
            await bot.send_message(int(i), msg)
            done += 1
        except:
            error += 1
    await xx.edit("Broadcast completed.\nSuccess: {}\nFailed: {}".format(done, error))
