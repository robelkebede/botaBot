
from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler,ConversationHandler
import telegram
import requests
import re
import datetime
import pymongo
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_client = pymongo.MongoClient("mongodb://localhost:27017/")  

mydb = db_client["Bota"]
seller_info = mydb["seller_info"]
product_info = mydb["product_info"]

global f_path
global f_pic

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

        try:

            db_chat_id = seller_info.find_one({"chat_id":chat_id})["chat_id"]

            return True
        except Exception as e:
            print("CHAT ID DONOT EXIST",e)
            return False

        
    def insert_user_to_database(self,bot,update):

        lat,lng = self.get_location(bot,update)
        chat_id = update.message.chat_id


        update.message.reply_text("welcome first time seller")

        update.message.reply_text("send your location ")

        location_keyboard = telegram.KeyboardButton(
                text="send_location", 
                request_location=True)

        custom_keyboard =[[ location_keyboard ]]

        reply_markup = telegram.ReplyKeyboardMarkup(
                custom_keyboard,
                one_time_keyboard=True)

        bot.send_message(chat_id=chat_id,
                text="Information",
                reply_markup=reply_markup
                )

        print("CDCDCDCDCDC ",[lat,lng])

        #optimize >>>
        #error handling in mycol.insert


        if lat and lng is None:
            print("the bot cant get the location ")

            update.message.reply_text("cant get the location ")
            
        else:
            #insert >>>
            print("this is a test for the register function")
            print("XSXSXSXSXSX ",[lat,lng,chat_id])

            if lat and lng and chat_id is not None:
                #check if the data is loded in to the database
                seller_info.insert({"chat_id":chat_id,"lat":lat,"lng":lng}) 
                update.message.reply_text("you are now registerd go to /start")
                #it is not going back
                return ConversationHandler.END





    def start(self,bot,update):
        
        chat_id = update.message.chat_id

        if self.chat_id_exists(chat_id):

            
            self.upload_product(bot,update)

        else:
            
            self.insert_user_to_database(bot,update)



    """
    def upload_product2(self,bot,update):
        
        update.message.reply_text("upload a picture of the product2")

        pic = None
        file_path = None
    
        chat_id = update.message.chat_id
        time = datetime.datetime.now()
        try:
            pic = update.message.photo[0].file_id
            file_path = bot.getFile(pic)["file_path"]
        except:
            print("inmage not yet sent")

        if file_path is not None:
            print("XAXAXAXAXAXAX ",file_path)
            update.message.reply_text("picture recieved")
            
            #uploaded with out description

            return ConversationHandler.END

    """  
    
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

            global f_path
            global f_pic

            f_path = file_path
            f_pic = pic

            update.message.reply_text("write a description")

        
        return new_server.UPLOAD_PIC

                
    def upload_product2(self,bot,update):

        global f_path
        global f_pic


        #find a way to delete this global variable

        description = update.message.text

        chat_id = update.message.chat_id
        time = datetime.datetime.now()

        if description is not None:
            print("description ",[f_path,description])
            #check if the data is sucessfuly loded in to the database
            product_info.insert({"chat_id":chat_id,"description":description,"pic_url":f_path,"f_pic":f_pic,"timestamp":time})

            update.message.reply_text("product uploaded")

            return ConversationHandler.END
            
        else:
            print([description])
    


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



