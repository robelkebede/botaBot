
import pymongo

client = pymongo.MongoClient("localhost", 27017, maxPoolSize=50)

db = client.Bota
collection = db['product_info']
collection1 = db['seller_info']

cursor = collection.find({})
cursor1 = collection1.find({})

product_data = [[]]

for document in cursor:
    product_data.append([document["chat_id"],document["timestamp"],document["pic_url"]])
    
del product_data[0]

for data in product_data:
    print(data[2])



