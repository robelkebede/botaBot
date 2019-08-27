

from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler
import telegram
import requests
import re
import queue
import pymongo
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_client = pymongo.MongoClient("mongodb://localhost:27017/")  


def get_location(bot,update):
    lat = None
    lng = None
    try:
        #lets not use phone for seller
        #phone = update.message.contact.phone_number
        lng = update.message.location.longitude
        lat = update.message.location.latitude
    except Exception as e:
        pass

    return lat,lng



def insert_to_database(bot,update):

    lat,lng = get_location(bot,update)

    chat_id = update.message.chat_id

    mydb = db_client["Bota"]
    mycol = mydb["seller_info"]

    if lat and lng is None:
        print("the bot cant get the location")

    else:
        db_chat_id = mycol.find_one({"chat_id":chat_id})["chat_id"]
        print("dbdbdb ",db_chat_id)
        if db_chat_id:
            #update
            print("UPDATE")
            old_data = {"chat_id":chat_id}
            new_data = {"$set":{"chat_id":chat_id,"lat":lat,"lng":lng}}
            
            mycol.update_one(old_data,new_data)
            

        else:
            mycol.insert({"chat_id":chat_id,"lat":lat,"lng":lng}) 
            print("INSERT")



def test_bot(bot,update):
    chat_id = update.message.chat_id

    location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
    contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[ location_keyboard, contact_keyboard ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    bot.send_message(chat_id=chat_id,
            text="Information",
            reply_markup=reply_markup
            )

    #phone = None
    insert_to_database(bot,update)


def upload_picture(bot,update):
    import datetime 

    chat_id = update.message.chat_id
    pic = update.message.photo[0].file_id
    time = datetime.datetime.now()
    file_path = bot.getFile(pic)["file_path"]

    mydb = db_client["Bota"]
    mycol = mydb["product_info"]


    mycol.insert({"chat_id":chat_id,"pic_url":file_path,"timestamp":time})

    update.message.reply_text("picture recieved")



def main():

    updater2 = Updater('971130326:AAFwIJEdclodQcpWNZtfEOjFXS_6qg5qusc')
    dp2 = updater2.dispatcher

    dp2.add_handler(MessageHandler(Filters.contact, test_bot))  
    dp2.add_handler(MessageHandler(Filters.location, test_bot))
    dp2.add_handler(MessageHandler(Filters.photo, upload_picture)) 
    dp2.add_handler(CommandHandler('start',test_bot))
    updater2.start_polling()
    updater2.idle()



if __name__ == '__main__':
    main()
