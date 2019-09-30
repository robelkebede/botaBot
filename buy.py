
from math import sin, cos, sqrt, atan2, radians
from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler,CallbackQueryHandler,ConversationHandler

from telegram import InlineKeyboardButton,InlineKeyboardMarkup
import telegram
import datetime
import logging
import pymongo
from sqlite_database_for_bota import fetch_product_data


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_client = pymongo.MongoClient("mongodb://localhost:27017/")  

db = db_client.Bota
user_data = db['user_data']



class Buy:

    def __init__(self):
        self.chat_id = None 
        self.lat = None
        self.lng = None

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


    def calculate_distance(self,user_lat,user_lng,product_lat,product_lng):

        R = 6373.0

        user_lat = radians(float(user_lat))
        user_lng = radians(float(user_lng))
        product_lat = radians(float(product_lat))
        product_lng = radians(float(product_lng))

        dlng = product_lng - user_lng
        dlat = product_lng - user_lng

        a = sin(dlat / 2)**2 + cos(user_lat) * cos(product_lat) * sin(dlng / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance


    def calculate_days(self,product_date,now):
        
        delta = now-product_date
        return delta.days


    

    def get_product(self):
        db = db_client.Bota
        collection = db['product_info']
        cursor = collection.find({})
        product_data = []


        for document in cursor:
            product_data.append(document)

        return product_data

    def get_product_from_sqlite(self):

        data = fetch_product_data()

        return data


    def filter_product(self,distance,day):

        #products = self.get_product()
        products = self.get_product_from_sqlite()
        print("THE PRODUCTSSSS ",products)
        time = datetime.datetime.now()
        filterd_products = []

        for product in products:
            lat,lng = product["lat"],product["lng"]
            timestamp = product["timestamp"]
            dis = self.calculate_distance(self.lat,self.lng,lat,lng)
            tim = self.calculate_days(timestamp,time)
            #problem hear
            if dis<distance and tim<day:
                filterd_products.append(product)


            print("dis and time",[dis,tim])

        return filterd_products 

        

    def start(self,bot,update):

        
        chat_id = update.message.chat_id
        self.chat_id = chat_id
        timestamp = datetime.datetime.now()
        
        location_keyboard = telegram.KeyboardButton(
                text="send_location", 
                request_location=True)

         
        custom_keyboard =[[ location_keyboard ]]

        reply_markup = telegram.ReplyKeyboardMarkup(
                custom_keyboard)

        bot.send_message(chat_id=chat_id,
                text="Information",
                reply_markup=reply_markup
                )

            
        lat,lng = self.get_location(bot,update)
        print("ASDASDASDASDASDAS  ",lat,lng) 

        self.lat = lat
        self.lng = lng


        if lat and lng is not None:
            
            #products = self.get_product()
            products_ = self.filter_product(10,10) 
            
            #better code

            print("PRODUCTTT ",products_)

            #bota consumers data
            #user_data.insert({"chat_id":chat_id,"timestamp":timestamp,"lat":lat,"lng":lng})

            for product in enumerate(products_):

                keyboard = [
                        [InlineKeyboardButton("location", callback_data=str(product[0]))]]
                
                reply_markup = InlineKeyboardMarkup(keyboard)

                bot.send_photo(chat_id=chat_id,photo=product[1]["pic_id"])
                update.message.reply_text(str(product[0])+", "+product[1]["description"],reply_markup=reply_markup)


            update.message.reply_text("this are products aroud you please \n i am /done")



    def location_button(self,bot,update):
        product_ = self.filter_product(10,10) 
        query = update.callback_query
        i = query.data #button clicked

        description = i+", "+product_[int(i)]["description"]
        lat =product_[int(i)]["lat"]
        lng =product_[int(i)]["lng"]

        bot.send_message(chat_id=self.chat_id,text=description)
        bot.send_location(chat_id=self.chat_id,latitude=lat,longitude=lng)


def main():

    updater = Updater('')
    dp = updater.dispatcher
    buy = Buy()
    dp.add_handler(CommandHandler('start',buy.start))
    dp.add_handler(CommandHandler('test',buy.test))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

