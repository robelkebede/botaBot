
from math import sin, cos, sqrt, atan2, radians
from telegram.ext import Updater,CommandHandler,Dispatcher,Filters,MessageHandler
import telegram
import datetime
import logging
import pymongo


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_client = pymongo.MongoClient("mongodb://localhost:27017/")  


class Buy:

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


    def calculate_distance(self,user_lat,user_lng,product_lat,product_lng):

        user_lat = radians(user_lat)
        user_lng = radians(user_lng)
        product_lat = radians(product_lat)
        product_lng = radians(product_lng)

        dlng = product_lng - user_lng
        dlat = product_lng - user_lng

        a = sin(dlat / 2)**2 + cos(user_lat) * cos(product_lat) * sin(dlng / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance


    def calculate_days(self,product_date,now):
        
        delta = now-product_date
        return delta.days


    def filter_product(self):
        pass


    def test(self,bot,update):
        update.message.reply_text("this is in object oreanted programming shit is at est")


    def get_product(self):
        db = db_client.Bota
        collection = db['product_info']
        cursor = collection.find({})
        product_data = [[]]


        for document in cursor:
             product_data.append([document["chat_id"],document["timestamp"],document["pic_url"]])

        del product_data[0]

        return product_data
        

    def start(self,bot,update):
        chat_id = update.message.chat_id
        
        location_keyboard = telegram.KeyboardButton(
                text="send_location", 
                request_location=True)

        contact_keyboard = telegram.KeyboardButton(
                text="send_contact", 
                request_contact=True)

        custom_keyboard =[[ location_keyboard, 
            contact_keyboard ]]

        reply_markup = telegram.ReplyKeyboardMarkup(
                custom_keyboard)

        bot.send_message(chat_id=chat_id,
                text="Information",
                reply_markup=reply_markup
                )

        lat,lng = get_location(bot,update)
        print("ASDASDASDASDASDAS  ",lat,lng) 

        #without Filter

        product_data = get_product()

        print("THEHTHEHTHEHTHETHT  ",product_data[1][2])

        
        #bot.send_photo(chat_id=chat_id,photo="https://api.telegram.org/file/bot971130326:AAFwIJEdclodQcpWNZtfEOjFXS_6qg5qusc/photos/file_4.jpg")

        update.message.reply_text("this are products aroud you")


        

def main():

    updater = Updater('893555483:AAHe1TXjMhEf6oFytXLYz4XEm9f47OlhSgI')
    dp = updater.dispatcher
    buy = Buy()
    dp.add_handler(CommandHandler('start',buy.start))
    dp.add_handler(CommandHandler('test',buy.test))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
