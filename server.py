import telegram
import logging
from buy import Buy
from sell import Sell

from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler,CallbackQueryHandler,ConversationHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#0 server,1 buy,2 sell
CHOOSE,BUY, SELL = range(3)


def test(bot,update):
    update.message.reply_text("the server is online")

def start_all(bot,update):


    chat_id = update.message.chat_id

    sell = telegram.KeyboardButton(text="buy")

    buy = telegram.KeyboardButton(text="sell")

    custom_keyboard =[[ sell, buy ]]

    reply_markup = telegram.ReplyKeyboardMarkup(
            custom_keyboard,one_time_keyboard=True)

    bot.send_message(chat_id=chat_id,
            text="Thank you",
            reply_markup=reply_markup
            )
    
    
    command= update.effective_message.text 

    print("TATATATATATATAT ",command)

    return CHOOSE

def sell(bot,update):
    print("THE SELL",update.effective_message.text )
    if update.effective_message.text == "sell":
        sell = Sell()

        return SELL


def buy(bot,update):
    if update.message.from_user == "buy":
        buy = Buy()


        return BUY

    """
    if command == "buy":
        
        buy = Buy()
        buy.start(bot,update)
    

    elif command == "sell":

        sell = Sell()
        sell.start(bot,update)

    else:
        print("TATATATATATATAT ",command)
    """




def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END

def main():

    updater = Updater('')

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('test',test))

    """
        
    #elif FLAG == 1:
    dp.add_handler(MessageHandler(Filters.location,buy.start),1)

    #elif FLAG == 2:
    dp.add_handler(MessageHandler(Filters.location, sell.insert_user_to_database))
    dp.add_handler(MessageHandler(Filters.photo, sell.upload_product2)) 
    dp.add_handler(MessageHandler(Filters.text, sell.upload_product2)) 

    """
    buy = Buy()
    sell = Sell()


    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start_all)],

             states={

                CHOOSE: [MessageHandler(Filters.regex('^(sell|buy)$'), start_all)],
                BUY: [MessageHandler(Filters.location,buy.start),
                      MessageHandler(Filters.text,buy.start)
                    ],
                SELL: [MessageHandler(Filters.location,sell.get_location),
                       MessageHandler(Filters.text,sell.start)
                       MessageHandler(Filters.photo,sell.start)
                       ]
                    

                },

                fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]

            )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
