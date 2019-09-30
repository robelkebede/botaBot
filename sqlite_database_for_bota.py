import sqlite3
from sqlite3 import Error
import datetime
import json

db_file = "./bota_database.db"

def create_connection(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn.cursor()


def create_table(db_file):

    conn = create_connection(db_file)

    #creata table product_data
    conn.execute("CREATE TABLE product_data (chat_id,description,pic_url,pic_id,timestamp,lat,lng)")

    conn.execute("CREATE TABLE user_data (chat_id,timestamp,lat,lng)")

    print("TABLE CREATE")



def insert_product(chat_id,description,pic_url,pic_id,timestamp,lat,lng):

    conn = sqlite3.connect('bota_database.db')
    cursor = conn.cursor() 

    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('INSERT INTO product_data (chat_id,description,pic_url,pic_id,timestamp,lat,lng) VALUES ("'+chat_id+'","'+description+'","'+pic_url+'","'+pic_id+'","'+timestamp+'","'+lat+'","'+lng+'") ')


    conn.commit()

    conn.close()

    print("PRODUCT INSERTD")

def insert_user_data(chat_id,timestamp,lat,lng):

    conn = sqlite3.connect('bota_database.db')
    cursor = conn.cursor() 


    #how to change strftime to datetime object
    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('INSERT INTO user_data (chat_id,timestamp,lat,lng) VALUES ("'+chat_id+'","'+timestamp+'","'+lat+'","'+lng+'") ')

    conn.commit()

    conn.close()

    print("USER INSERTD")


def fetch_product_data():

    conn = sqlite3.connect('bota_database.db')
    cursor = conn.cursor() 

    data=cursor.execute("SELECT * FROM product_data").fetchall()
    final_data = []

    for d in data:

        datetime_obj = datetime.datetime.strptime(d[4],'%Y-%m-%d %H:%M:%S')

        d = {"chat_id":d[0],"description":d[1],"pic_url":d[2],"pic_id":d[3],"timestamp":datetime_obj,"lat":d[5],"lng":d[6]}
        final_data.append(d) 

    conn.close()

    print("FETCH ALL DATA")
    return final_data


if __name__ == "__main__":

    print("RUNNING FOR THE FIRST TIME")
    create_connection(db_file)
    create_table(db_file)



    #print(data[0]["chat_id"])

    #insert_product('asd','the real deal','1234','4234',datetime.datetime.now(),'23423','234')
