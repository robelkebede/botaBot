import telegram
import logging

from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



def test(bot,update):
    update.message.reply_text("the server is  online")

def start(bot,update):
    chat_id = update.message.chat_id
    
    location_keyboard = telegram.KeyboardButton(
            text="buy")

    contact_keyboard = telegram.KeyboardButton(text="sell")

    custom_keyboard =[[ location_keyboard, 
        contact_keyboard ]]

    reply_markup = telegram.ReplyKeyboardMarkup(
            custom_keyboard)

    bot.send_message(chat_id=chat_id,
            text="Thank you",
            reply_markup=reply_markup
            )

    command= update.effective_message.text 

    print("TATATATATATATAT ",command)

    if command == "buy":
        pass
    else if command == "sell":
        pass
    else:
        pass






def main():

    updater = Updater('893555483:AAHe1TXjMhEf6oFytXLYz4XEm9f47OlhSgI')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('test',test))
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(MessageHandler(Filters.text, start))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

