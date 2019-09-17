import telegram
import logging
from buy import Buy
from sell import Sell

from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler,CallbackQueryHandler,ConversationHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#0 server,1 buy,2 sell
CHOOSE,BUY, SELL,UPLOAD_PIC = range(4)


def start_all(bot,update):
    
    reply_keyboard = [['buy', 'sell']]

    #get the name of the user
 
    update.message.reply_text(
        'Hi! My name is Bota. I will hold a conversation with you. '
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
        STATE = 0

    return STATE



def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def done(update, context):
    user_data = context.user_data

    return ConversationHandler.END

def main():

    updater = Updater('893555483:AAGdRO8sruE8lVrCBrd8GnlBrj1W28_Sit0')

    dp = updater.dispatcher
    buy = Buy()
    sell = Sell()

    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start_all)],

             states={

                 CHOOSE: [MessageHandler(Filters.regex('^(buy|sell)$'), choice)],
                 BUY: [MessageHandler(Filters.location,buy.start)],

                 SELL: [MessageHandler(Filters.location,sell.start),
                       MessageHandler(Filters.photo,sell.upload_product), #make this sell.product_upload
                       ],
                 UPLOAD_PIC:[
                       MessageHandler(Filters.text,sell.upload_product2), #make this sell.product_upload
                     ]
                 
                 
            },
                 fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
            )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
