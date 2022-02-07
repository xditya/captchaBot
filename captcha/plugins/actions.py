# (c) 2022 @xditya.
# Powered by apis.xditya.me

import re

from requests import get
from captcha.plugins.database_fns import add_to_db, del_from_db, is_added
from . import events, bot, Button
from . import db
from .. import log

# listen to new joins
@bot.on(events.ChatAction)
async def on_user_added(event):
    user = await event.get_user()
    cache_opts = eval(db.get("CACHE"))

    if (event.user_left or event.user_kicked) and user.id == (await bot.get_me()).id:
        if is_added("group", event.chat_id):
            del_from_db("group", event.chat_id)
        return

    if not (event.user_joined or event.added_by):
        # ignore events other than user joins
        return
    if user.id == (await bot.get_me()).id:
        await event.reply(
            "Hey, thanks for adding me here. Learn how to use me by clicking the below button!",
            buttons=[Button.inline("Usage guide", data="help")],
        )
        if not is_added("group", event.chat_id):
            add_to_db("group", event.chat_id)
        return

    if user.bot:
        return

    try:
        await bot.edit_permissions(
            event.chat_id,
            user.id,
            until_date=None,
            send_messages=False,
        )
    except:
        # cant mute, not an admin !
        return

    try:
        data = get("https://apis.xditya.me/captcha?options=6").json()
    except Exception as e:
        log.exception(e)
        return

    pic = data["captcha"]
    options = data["options"]
    answer = data["correct"]

    t = f"{event.chat_id}|{user.id}"
    cache_opts.update({t: answer})
    db.set("CACHE", str(cache_opts))

    buttons_row = [Button.inline(i, data="a_{}||{}".format(i, t)) for i in options]
    buttons = []
    while buttons_row:
        buttons.extend([buttons_row[:2]])
        buttons_row = buttons_row[2:]

    await event.reply(
        "Hi {}. Please solve the captcha to be able to speak here!".format(
            user.first_name
        ),
        file=pic,
        buttons=buttons,
    )


@bot.on(events.CallbackQuery(data=re.compile("a_(.*)")))
async def unmuter(event):
    args = event.data_match.group(1).decode("UTF-8")
    clicked, info = args.split("||")
    cache_opts = eval(db.get("CACHE"))
    answer = cache_opts.get(info)
    user = int(info.split("|")[1])

    if event.sender_id != user:
        return await event.answer("This is not for you 😠")
    if not answer:
        await event.answer("Something went wrong! Rejoin the group.", alert=True)
        return
    else:
        if clicked != answer:
            return await event.answer("Wrong choice, are you a bot?")
        await bot.edit_permissions(
            event.chat_id,
            user,
            send_messages=True,
        )
        await event.answer("Congrats!")
        await event.reply(
            "Hey {}, welcome to the group!".format(
                (await bot.get_entity(user)).first_name
            )
        )
        await event.delete()
