import telegram
import logging
from buy import Buy
from sell import Sell

from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler,CallbackQueryHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#0 server,1 buy,2 sell

global FLAG 

FLAG = 10


def test(bot,update):
    update.message.reply_text("the server is online")

def start_all(bot,update):
    chat_id = update.message.chat_id

    FLAG = 0
    
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


    if command == "buy":
        buy = Buy()
        FLAG = 1
        buy.start(bot,update)

    elif command == "sell":
        sell = Sell()
        FLAG = 2
        sell.start(bot,update)

    else:
        #help
        pass



def main():

    updater = Updater('893555483:AAHe1TXjMhEf6oFytXLYz4XEm9f47OlhSgI')


    dp = updater.dispatcher
    dp.add_handler(CommandHandler('test',test))

    #if FLAG is 0,1 or 2
    print("THE REAL FLAG ",FLAG)

    if FLAG == 1:
        buy = Buy()
        dp.add_handler(MessageHandler(Filters.location, 
        buy.start))
   

    elif FLAG == 2:
        sell = Sell()
        dp.add_handler(MessageHandler(Filters.location, sell.insert_user_to_database)) 
        dp.add_handler(MessageHandler(Filters.photo, sell.upload_product2)) 
        dp.add_handler(MessageHandler(Filters.text, sell.upload_product2)) 


    elif FLAG == 0:
        dp.add_handler(CommandHandler('start',start_all))
        print("THIS HIOS")

    else:
        print("NONONONONONONONONON",FLAG)


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
