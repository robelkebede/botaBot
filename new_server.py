import telegram
import logging
from buy import Buy
from sell import Sell

from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler,CallbackQueryHandler,ConversationHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#0 server,1 buy,2 sell
CHOOSE,BUY, SELL,UPLOAD_PIC,FINAL_LOC = range(5)


def start_all(bot,update):
    
    reply_keyboard = [['buy', 'sell']]

    #get the name of the user

    name = update.message.from_user.first_name
 
    update.message.reply_text(
        'Hi '+name+' ! My name is Bota. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'do you want to sell or buy?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
 
    return CHOOSE


def choice(bot,update):

    res = update.message.text

    STATE =None

    buy = Buy()
    sell = Sell()

    if res == "sell":

        STATE = SELL
        sell.start(bot,update)

    elif res=="buy":

        STATE = BUY
        buy.start(bot,update)
    else:
        pass

    return STATE



def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def done(bot, update):
    
    #user_data = context.user_data
    update.message.reply_text("Thank you go to /start")

    return ConversationHandler.END

def main():

    updater = Updater('')

    dp = updater.dispatcher
    buy = Buy()
    sell = Sell()

    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start_all)],

             states={

                 CHOOSE: [MessageHandler(Filters.regex('^(buy|sell)$'), choice)],
                 BUY: [MessageHandler(Filters.location,buy.start),
                        CallbackQueryHandler(buy.location_button)
                     ],

                 SELL: [MessageHandler(Filters.location,sell.start),
                       MessageHandler(Filters.photo,sell.upload_product), 
                       ],
                 UPLOAD_PIC:[
                       MessageHandler(Filters.text,sell.upload_product2),
                     ],
                 FINAL_LOC:[
                       MessageHandler(Filters.location,sell.final_),
                  ]
                 
                 
            },
             fallbacks=[CommandHandler('done', done)]
            )


    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()



if __name__ == "__main__":
    main()
