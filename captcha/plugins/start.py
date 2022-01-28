# (c) 2022 @xditya.
# Powered by apis.xditya.me

from . import bot, events, Button
from .db import is_added, add_to_db


@bot.on(events.NewMessage(incoming=True, pattern=r"^/start ?(.*)"))
async def starters(event):
    args = event.pattern_match.group(1)

    if not event.is_private:
        await event.reply(
            "Contact me in PM for that.",
            buttons=Button.inline("Contact me in PM!", data="help"),
        )
    else:
        if not is_added("users", event.sender_id):
            add_to_db("users", event.sender_id)

        if args == "help":
            await event.reply(
                "**Here is how to use me:**\n\n- Add me to a group by pressing the below button.\n- Make me admin with mute users permission.\n- [**OPTIONAL**] Use /setwelcome to set your custom welcome message.\n\nThats it! The bot is configured, and is ready to be used!!",
                buttons=[
                    [
                        Button.url(
                            "➕ Add me to a group",
                            url="http://t.me/{}?startgroup=true".format(
                                (await bot.get_me()).username
                            ),
                        )
                    ],
                    [Button.url("Support", url="https://t.me/BotzHubChat")],
                ],
            )
            return
        await event.reply(
            "Hi {}, I'm a captcha bot.\nAdd me to a group with `mute` permissions, and I'll activate join captcha for your group.".format(
                (await bot.get_entity(event.chat_id)).first_name
            ),
            buttons=[
                [
                    Button.url(
                        "➕ Add me to a group",
                        url="http://t.me/{}?startgroup=true".format(
                            (await bot.get_me()).username
                        ),
                    )
                ],
                [
                    Button.inline("Help", data="help"),
                    Button.url("Updates", url="https://t.me/BotzHub"),
                ],
                [Button.url("Repository", url="https://github.com/xditya/captchaBot")],
            ],
        )


@bot.on(events.CallbackQuery(data="help"))
async def start_callback(event):
    if not is_added("users", event.sender_id):
        add_to_db("users", event.sender_id)
    await event.answer(
        url="t.me/{}?start=help".format((await bot.get_me()).username), cache_time=0
    )
