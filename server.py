from telegram.ext import Updater,CommandHandler
import telegram
import requests
import re


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def bop(bot, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    print(chat_id)
    bot.send_photo(chat_id=chat_id, photo=url)

def sendLocation(bot,update):
    location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
    contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[ location_keyboard, contact_keyboard ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    chat_id = update.message.chat_id


    bot.send_message(chat_id=chat_id,
            text="we need your location",
            reply_markup=reply_markup
            )
    print(update.message)


def dataStore():
    pass


def main():
    updater = Updater('893555483:AAHe1TXjMhEf6oFytXLYz4XEm9f47OlhSgI')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('loca',sendLocation))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
