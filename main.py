from datetime import datetime
from telegram.ext import *


def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi", "hey", "sup", "supp", "hola"):
        return "Hey! whats up?"
    if user_message in ("time", "date", "time?", "date?"):
        systemTime = datetime.now().strftime("%d/%m/%y , %H:%M:%S")
        return systemTime
    if user_message in ("what is your name?", "who are you", "what are you"):
        return "I am a bot created by Mihir thanks for asking."
    return "Sorry I don't get you"


def start_command(update, context):
    update.message.reply_text("Write Hi to get started with")


def help_command(update, context):
    update.message.reply_text("I can understand greetings and you can ask me for time and date.")


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = sample_responses(text)
    update.message.reply_text(response)


def errorCollection(update, context):
    print(f'Update {update} caused error {context.error}')


def main():
    updater = Updater("your bot token here", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", start_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(errorCollection)

    updater.start_polling()
    updater.idle()


main()
