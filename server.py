import telegram
import logging
from buy import Buy
from sell import Sell

from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler,CallbackQueryHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test(bot,update):
    update.message.reply_text("the server is online")

def start_all(bot,update):
    chat_id = update.message.chat_id

    sell = telegram.KeyboardButton(text="buy")

    buy = telegram.KeyboardButton(text="sell")

    custom_keyboard =[[ sell, buy ]]

    reply_markup = telegram.ReplyKeyboardMarkup(
            custom_keyboard)

    bot.send_message(chat_id=chat_id,
            text="Thank you",
            reply_markup=reply_markup
            )
    
    
    command= update.effective_message.text 

    print("TATATATATATATAT ",command)

    buy = Buy()
    sell = Sell()

    if command == "buy":
        
        buy.start(bot,update)

    elif command == "sell":

        sell.start(bot,update)

    else:
        #help
        pass



def main():

    updater = Updater('893555483:AAHe1TXjMhEf6oFytXLYz4XEm9f47OlhSgI')

    buy = Buy()
    sell = Sell()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('test',test))
    dp.add_handler(MessageHandler(Filters.location, 
        buy.start))
    dp.add_handler(CommandHandler('start',start_all))
    dp.add_handler(CallbackQueryHandler(start_all))
    dp.add_handler(MessageHandler(Filters.text, start_all))

    dp.add_handler(MessageHandler(Filters.location, sell.insert_user_to_database)) 
    dp.add_handler(MessageHandler(Filters.photo, sell.upload_product2)) 
    dp.add_handler(MessageHandler(Filters.text, sell.upload_product2)) 
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

