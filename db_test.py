
import pymongo

client = pymongo.MongoClient("localhost", 27017, maxPoolSize=50)

db = client.Bota
product_info = db['product_info']
seller_info = db['seller_info']

def show_all():

    cursor = product_info.find({})
    cursor1 = seller_info.find({})

    product_data = [[]]

    for document in cursor:
        print(document)

        
    #del product_data[0]


def delete_all():
    product_info.remove({})
    seller_info.remove({})

def find_one():

    try:

        db_chat_id = seller_info.find_one({"chat_id":23})["chat_id"]

        print(db_chat_id)
    except Exception as e:
        print(e)
        
    

def main():
    show_all()
    #find_one()
    #delete_all()


if __name__ == "__main__":
    main()
