
import pymongo

client = pymongo.MongoClient("localhost", 27017, maxPoolSize=50)

db = client.Bota
collection = db['product_info']
cursor = collection.find({})

for document in cursor:
    print(document)
