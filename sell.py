

from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler
import telegram
import requests
import re
import datetime
import queue
import pymongo
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_client = pymongo.MongoClient("mongodb://localhost:27017/")  

mydb = db_client["Bota"]
mycol = mydb["seller_info"]



class Sell:
    def __init__(self):
        pass


    def get_location(self,bot,update):
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

    def chat_id_exists(self,chat_id):
        db_chat_id = mycol.find_one({"chat_id":chat_id})["chat_id"]

        print("chaeck if chat id exists ",chat_id)

        if chat_id is not None:
            return True
        else:
            return False


    def insert_to_database(self,bot,update):

        lat,lng = self.get_location(bot,update)

        chat_id = update.message.chat_id


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



    def test_bot(self,bot,update):
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
        if self.chat_id_exists(chat_id):
            #upload a picture 
            #and descriptioA
            pass
        else:
            #wel come first time seller

            #location
            #phone
            # if this both thing exists insert into database
            #start /sell command
            pass

        insert_to_database(bot,update)



    def test(self,bot,update):
        update.message.reply_text("this is in object oreanted programming shit is at est")


    def upload_picture(self,bot,update):

        chat_id = update.message.chat_id
        time = datetime.datetime.now()
        file_path = bot.getFile(pic)["file_path"]

        mydb = db_client["Bota"]
        mycol = mydb["product_info"]


        mycol.insert({"chat_id":chat_id,"pic_url":file_path,"timestamp":time})

        update.message.reply_text("picture recieved")



def main():

    updater2 = Updater('971130326:AAFwIJEdclodQcpWNZtfEOjFXS_6qg5qusc')
    dp2 = updater2.dispatcher
    sell = Sell()

    dp2.add_handler(MessageHandler(Filters.contact, sell.test_bot))  
    dp2.add_handler(MessageHandler(Filters.location, sell.test_bot))
    dp2.add_handler(MessageHandler(Filters.photo, sell.upload_picture)) 
    dp2.add_handler(CommandHandler('start',sell.test_bot))
    dp2.add_handler(CommandHandler('test',sell.test))
    updater2.start_polling()
    updater2.idle()



if __name__ == '__main__':
    main()
