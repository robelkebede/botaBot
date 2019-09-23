
from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler,ConversationHandler
import telegram
import requests
import re
import datetime
import pymongo
import logging
from sqlite_database_for_bota import insert_product



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_client = pymongo.MongoClient("mongodb://localhost:27017/")  

mydb = db_client["Bota"]
seller_info = mydb["seller_info"]
product_info = mydb["product_info"]

class Sell:
    def __init__(self):
        self.f_path = None
        self.f_pic = None
        self.description = None
        

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



    def start(self,bot,update):
        
        self.upload_product(bot,update)


    
    def upload_product(self,bot,update):
        
        update.message.reply_text("upload a picture of the product")
        import new_server
    
        pic = None
        file_path = None
        description = None
    
        
        try:
            pic = update.message.photo[0].file_id
            file_path = bot.getFile(pic)["file_path"]
        except:
            print("image not yet sent")


        if file_path is not None:
            print("XAXAXAXAXAXAX ",file_path)
            update.message.reply_text("picture recieved")

            self.f_path = file_path
            self.f_pic = pic

            update.message.reply_text("write a description")

        
        return new_server.UPLOAD_PIC

                    
    def upload_product2(self,bot,update):

        
        import new_server

        chat_id = update.message.chat_id

        description = update.message.text
        self.description = description


        print("DESCRIPTION ",self.description)

        
        update.message.reply_text("description updated now send your location")

        location_keyboard = telegram.KeyboardButton(
                text="send_location", 
                request_location=True)

        custom_keyboard =[[ location_keyboard ]]

        reply_markup = telegram.ReplyKeyboardMarkup(
                custom_keyboard,
                one_time_keyboard=True)

        bot.send_message(chat_id=chat_id,
                text = "info",
                reply_markup=reply_markup
                )


        return new_server.FINAL_LOC 


    def final_(self,bot,update):


        lat,lng = self.get_location(bot,update)
        chat_id = update.message.chat_id
        time = datetime.datetime.now()
        description = self.description
        pic_url = self.f_path
        pic_id = self.f_pic

        if None not in (lat,lng,chat_id,time,description,pic_url,pic_id):


            product_info.insert({"chat_id":chat_id,"description":description,"pic_url":pic_url,"pic_id":pic_id,"timestamp":time,"lat":lat,"lng":lng})
            
            #insert_product(chat_id,description,pic_url,pic_id,timestamp,lat,lng)

            print([lat,lng,chat_id,time,description,pic_url,pic_id])

            update.message.reply_text("product uploaded")

            return ConversationHandler.END






def main():

    updater2 = Updater('971130326:AAFwIJEdclodQcpWNZtfEOjFXS_6qg5qusc')
    dp2 = updater2.dispatcher
    sell = Sell()

    dp2.add_handler(MessageHandler(Filters.contact, sell.test_bot))  
    dp2.add_handler(MessageHandler(Filters.location, sell.test_bot))
    dp2.add_handler(MessageHandler(Filters.photo, sell.upload_picture)) 
    dp2.add_handler(CommandHandler('start',sell.start))
    dp2.add_handler(CommandHandler('test',sell.test))
    updater2.start_polling()
    updater2.idle()



