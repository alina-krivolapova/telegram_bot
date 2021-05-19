import logging
import ephem

from random import randint, choice
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from emoji import emojize
from datetime import date

import connection_settings

from settings import pies, user_emoji, list_of_planets

logging.basicConfig(filename='bot.log', level=logging.INFO)


def add_smile() -> str:
    """Add smile."""
    return emojize(choice(user_emoji), use_aliases=True)


def greet_user(update: Update, context: CallbackContext) -> None:
    """Greet user and provide info about specific requests accepted by bot."""
    print("/Start was activated")
    update.message.reply_text("Превед Медвед! Ты пирожок \n"
                              "Используй следующий команды, чтобы выяснить подробьности: \n"
                              "/info <имя_пирожка> -  информация о пирожке \n"
                              "/planet <имя планеты>  - в каком созвездии находится планете, откуда прилетел пирожок")


def talk_to_me(update: Update, context: CallbackContext) -> None:
    """Accept any text specified by user and provide an answer."""
    print("Talking")
    user_text = update.message.text
    if ("ты" or "сам") in user_text.lower():
        update.message.reply_text("А чо это я сразу?")
    print(user_text)
    i = randint(0, 14)  # 14 is added to enlarge frequency of printing direct answer
    if i > 8:
        update.message.reply_text(f"Я все про тебя знаю {update.effective_user.first_name}!")
        i -= 10
    update.message.reply_text(pies[i])


def provide_info(update: Update, context: CallbackContext) -> None:
    """Handle pie info requests from user."""
    print("/Info request was activated")
    if context.args:
        message = f"Ага, пирожок {context.args[0]} найден! Но он секретный! {add_smile()}"
    else:
        message = "Надо сразу вводить имя пирожка, так ничего не получится!"
    update.message.reply_text(message)


def provide_planet_info(update: Update, context: CallbackContext) -> None:
    """Handle planet info requests from user.

    Function checks planet name and returns todays constellantion of planet.
    """

    print("/Planet info request was activated")
    # it's easier to use context.args, but it's requested to use update.message.text & split
    user_input = update.message.text.split()
    if len(user_input) == 1:
        update.message.reply_text("Нужно сразу ввести имя планеты!")
    else:
        planet = user_input[1].capitalize()
        if planet in list_of_planets:
            if planet == "Earth":
                update.message.reply_text("Я ничего не знаю про Землю, попробуй еще раз")
            else:
                update.message.reply_text(ephem.constellation(getattr(ephem, planet)(date.today()))[1])
        else:
            update.message.reply_text("Такой планеты не существует!")


def main() -> None:
    """Create bot and add all high-level instructions."""
    # Create bot and give him a connection key
    mybot = Updater(connection_settings.API_KEY, use_context=True)

    db = mybot.dispatcher
    db.add_handler(CommandHandler("start", greet_user))
    db.add_handler(CommandHandler("info", provide_info))
    db.add_handler(CommandHandler("planet", provide_planet_info))
    db.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot was started")
    # Bot starts to connect Telegram services looking for messages
    mybot.start_polling()
    # Bot should work until intentional stop
    mybot.idle()


if __name__ == "__main__":
    main()
