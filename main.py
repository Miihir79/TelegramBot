from datetime import datetime
from telegram.ext import *
import requests
import pandas as pd


def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi", "hey", "sup", "supp", "hola"):
        return "Hey! mihir here whats up?"
    if user_message in ("time", "date", "time?", "date?"):
        systemTime = datetime.now().strftime("%d/%m/%y , %H:%M:%S")
        return systemTime
    if user_message in ("what is your name?", "who are you", "what are you"):
        return "I am a bot created by Mihir thanks for asking."
    if user_message in ("what's your mood like?", "how is your mood?", "what are you feeling"):
        return "As you have asked I am in a better mood"
    if user_message == "eth":
        message = get_crypto_data("INR", "ETH")
        return f' 1 ETH ={message} INR'
    if user_message == "btc":
        message = get_crypto_data("INR", "BTC")
        return f' 1 BTC ={message} INR'
    return "Sorry I don't get you"


def start_command(update, context):
    update.message.reply_text("Write Hi to get started with")


def help_command(update, context):
    update.message.reply_text("I can understand greetings and you can ask me for time and date, \n Type ETH,"
                              "BTC to get price in INR.")


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = sample_responses(text)
    update.message.reply_text(response)


def errorCollection(update, context):
    print(f'Update {update} caused error {context.error}')


API_KEY = "118DB0CD-105C-4F12-9532-81A626E6A16C"


def get_crypto_data(currencyFun="USD", crypto="BTC", invert='true'):
    url = f'https://rest.coinapi.io/v1/exchangerate/{currencyFun}?invert={invert}'
    headers = {'X-CoinAPI-Key': API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()

    assets_names, assets_rates = [], []

    for asset in data['rates']:
        asset_id = asset['asset_id_quote']
        rate = asset['rate']

        assets_names.append(asset_id)
        assets_rates.append(rate)

    raw_data = {
        'assets': assets_names,
        'rates': assets_rates
    }
    df_coin = pd.DataFrame(raw_data)

    value = df_coin.loc[df_coin.assets == crypto, 'rates'].tolist()[0]

    return value


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