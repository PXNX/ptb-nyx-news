import logging
from uuid import uuid4

import requests
from telegram import Update, BotCommandScopeChat, ReplyKeyboardMarkup, WebAppInfo, KeyboardButton, \
    InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultsButton
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Application, CommandHandler, filters
from telegram.helpers import mention_html

from bot. settings.config import ADMINS, ADMIN_GROUP, ADMIN_GROUPS
from bot. util.helper import reply_photo, reply_html




async def maps(update: Update, context: CallbackContext):
    await reply_html(update, context, "maps")


async def loss(update: Update, context: CallbackContext):
    await reply_html(update, context, "loss")


async def stats(update: Update, context: CallbackContext):
    await reply_html(update, context, "stats")


async def short(update: Update, context: CallbackContext):
    await reply_html(update, context, "short")

    await update.message.reply_text("Viel Spaß mit der crappy Website xddd", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton("Öffne mich hart!", web_app=WebAppInfo("https://4142-91-33-115-20.ngrok-free.app"))]
    ], resize_keyboard=True, one_time_keyboard=True))


async def inline_query(update: Update, _: CallbackContext):
    query = update.inline_query.query
    if not query:
        return

    await update.inline_query.answer(
        button=InlineQueryResultsButton("open app", WebAppInfo("https://4142-91-33-115-20.ngrok-free.app")),

        results=[InlineQueryResultArticle(
            id=str(uuid4()),
            title="short",
            input_message_content=InputTextMessageContent("hi"),
            #  url="https://4142-91-33-115-20.ngrok-free.app",

            #  hide_url=True
        ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="map",
                input_message_content=InputTextMessageContent("hi"),
                url="https://telegra.ph/russland-ukraine-statistik-methodik-quellen-02-18",

                #  hide_url=True
            ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="mapthumb",
                input_message_content=InputTextMessageContent("hi"),
                thumbnail_url="https://telegra.ph/file/87aa41b45b907a5135052.png",
                url="https://telegra.ph/russland-ukraine-statistik-methodik-quellen-02-18",

                #  hide_url=True
            )
        ]

    )


async def donbass(update: Update, context: CallbackContext):
    await reply_html(update, context, "donbass")


async def channels(update: Update, context: CallbackContext):
    await reply_html(update, context, "channels")


async def genozid(update: Update, context: CallbackContext):
    await reply_html(update, context, "genozid")


async def peace(update: Update, context: CallbackContext):
    await reply_html(update, context, "peace")


async def support(update: Update, context: CallbackContext):
    await reply_photo(update, context, "support_ua.jpg", "support")


async def admin(update: Update, context: CallbackContext):
    logging.info(f"admin msg: {update.message}")

    try:
        await update.message.delete()
    except Exception:
        logging.error(f"Could not delete message {update.message}")

    if update.message.reply_to_message is not None:
        if update.message.reply_to_message.is_automatic_forward:
            text = f"💬  <a href='{update.message.reply_to_message.link}'>Kanalpost</a>"
            response = "Danke für deine Meldung, wir Admins prüfen das 😊"
        else:
            text = f"‼️ <a href='{update.message.reply_to_message.link}'>Nachricht</a> des Nutzers {update.message.reply_to_message.from_user.mention_html()}"
            response = "Ein Nutzer hat deine Nachricht gemeldet. Wir Admins prüfen das."

        text += f" gemeldet von {update.message.from_user.mention_html()}:\n\n"

        if update.message.reply_to_message.caption is not None:
            text += update.message.reply_to_message.caption_html_urled
        else:
            text += update.message.reply_to_message.text_html_urled

        target_group = ADMIN_GROUPS[update.message.chat_id]
        thread_id = None
        if target_group == ADMIN_GROUP:
            thread_id = 206
            response += "\n\nBitte beachte, dass diese Gruppe eigentlich nicht zu chatten gedacht ist."

        await context.bot.send_message(target_group, text, message_thread_id=thread_id)

        await update.message.reply_to_message.reply_text(response)


async def sofa(update: Update, context: CallbackContext):
    await reply_photo(update, context, "sofa.jpg")


async def bot(update: Update, context: CallbackContext):
    await reply_photo(update, context, "bot.jpg")


async def mimimi(update: Update, context: CallbackContext):
    await reply_photo(update, context, "mimimi.jpg")


async def cia(update: Update, context: CallbackContext):
    await reply_photo(update, context, "cia.jpg")


async def start(update: Update, context: CallbackContext):
    await reply_html(update, context, "start")


async def unwarn_user(update: Update, context: CallbackContext):
    await update.message.delete()

    if update.message.from_user.id in ADMINS and update.message.reply_to_message is not None and update.message.reply_to_message.from_user.id not in ADMINS:
        logging.info(f"unwarning {update.message.reply_to_message.from_user.id} !!")
        if "users" not in context.bot_data or update.message.reply_to_message.from_user.id not in context.bot_data[
            "users"] or "warn" not in context.bot_data["users"][update.message.reply_to_message.from_user.id]:
            warnings = 0
            context.bot_data["users"] = {update.message.reply_to_message.from_user.id: {"warn": warnings}}

        else:
            warnings = context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"]

            if warnings != 0:
                warnings = warnings - 1

            context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"] = warnings

            await update.message.reply_to_message.reply_text(
                f"Dem Nutzer {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} wurde eine Warnung erlassen, womit er nur noch {warnings} von 3 hat.")


async def warn_user(update: Update, context: CallbackContext):
    await update.message.delete()

    if update.message.from_user.id in ADMINS and update.message.reply_to_message is not None and update.message.reply_to_message.from_user.id not in ADMINS:
        logging.info(f"warning {update.message.reply_to_message.from_user.id} !!")
        if "users" not in context.bot_data or update.message.reply_to_message.from_user.id not in context.bot_data[
            "users"] or "warn" not in context.bot_data["users"][update.message.reply_to_message.from_user.id]:
            warnings = 1
            context.bot_data["users"] = {update.message.reply_to_message.from_user.id: {"warn": warnings}}

        else:
            warnings = context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"]
            if warnings == 3:
                logging.info(f"banning {update.message.reply_to_message.from_user.id} !!")
                await context.bot.ban_chat_member(update.message.reply_to_message.chat_id,
                                                  update.message.reply_to_message.from_user.id, until_date=1)
                await update.message.reply_to_message.reply_text(
                    f"Aufgrund wiederholter Verstöße habe ich {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} gebannt.")
                return
            else:
                warnings = warnings + 1
                context.bot_data["users"][update.message.reply_to_message.from_user.id]["warn"] = warnings

        warn_Text = f"Der Nutzer {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)} hat die Warnung {warnings} von 3 erhalten."
        if len(context.args) != 0:
            warn_text = f"{warn_Text}\n\nGrund: {' '.join(context.args)}"
        else:
            warn_text = f"Hey! Das musste jetzt echt nicht sein. Bitte verhalte dich besser!\n\n{warn_Text}"

        await update.message.reply_to_message.reply_text(warn_text)


async def report_user(update: Update, _: CallbackContext):
    await update.message.delete()

    if update.message.from_user.id in ADMINS and update.message.reply_to_message is not None and update.message.reply_to_message.from_user.id not in ADMINS:
        logging.info(f"reporting {update.message.reply_to_message.from_user.id} !!")
        r = requests.post(url="http://localhost:8080/reports",
                          json={
                              "user_id": update.message.reply_to_message.from_user.id,
                              "message": update.message.reply_to_message.text_html_urled,
                              "account_id": 1
                          })
        logging.info(r)
        await update.message.reply_to_message.reply_text(
            f"Hey {mention_html(update.message.reply_to_message.from_user.id, update.message.reply_to_message.from_user.first_name)}!\n\nEin Admin dieser Gruppe hat deinen Account unserem Antispam-System gemeldet. Moderatoren überprüfen diesen Fall nun.\n\nFalls dein Account Betrug oder Spam begangen hat, dann wirst du in allen Gruppen gebannt, wenn unser Antispam-System dort aktiv ist.")


def register_commands(app: Application):
    app.add_handler(CommandHandler("maps", maps))
    app.add_handler(CommandHandler("donbass", donbass))
    app.add_handler(CommandHandler("loss", loss))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("short", short))
    app.add_handler(CommandHandler("peace", peace))
    app.add_handler(CommandHandler("channels", channels))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(CommandHandler("genozid", genozid))

    app.add_handler(CommandHandler("sofa", sofa))
    app.add_handler(CommandHandler("bot", bot))
    app.add_handler(CommandHandler("mimimi", mimimi))
    app.add_handler(CommandHandler("cia", cia))


    app.add_handler(CommandHandler("start", start, filters.ChatType.PRIVATE))
