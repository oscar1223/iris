###
# Class that contains the necessary methods to perform CRUD operations against the database
###
import re
from datetime import datetime

from modules import var_c
import pymongo
from modules.compress import compressBson
from modules.compress import image_to_base
from modules.er import get_time_stamp, create_custom_regex
from modules.var_c import MONGO_U_CREDITS_COLLECTION, MONGO_IMAGE_COLLECTION, MONGO_IP, MONGO_DATABASE_NAME, \
    MONGO_U_PAY_COLLECTION, MONGO_U_PERMISSIONS_COLLECTION


# Method that search the database for a coincidence whit the hash of the uploaded image
def hash_finder(hash):
    myclient = pymongo.MongoClient(MONGO_IP)
    mydb = myclient[MONGO_DATABASE_NAME]
    mycol = mydb[MONGO_IMAGE_COLLECTION]
    myquery = {"hash_img": hash}

    mydoc = mycol.find(myquery)

    if len(list(mydoc)) == 0:
        return True
    else:
        return False


# Insert method
def insert_query(time_stamp, hash_img, text, source, name, data, image):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_IMAGE_COLLECTION]

    Bson_image = image_to_base(image)

    Bson_image = compressBson(Bson_image)

    row = {'time_stamp': time_stamp, 'hash_img': hash_img, 'text': text, 'source': source, 'name': name, 'data': data,
           'image': Bson_image}

    mycollection.insert_one(row)

    return row


# Search method
def find_words(word):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_IMAGE_COLLECTION]

    match_list = []

    for rows in mycollection.find():

        if word in rows['data']["nombres"][0]:
            print("Encontrado")
            match_list.append(rows)
        elif word in rows['data']["nombres"][1]:
            print("Encontrado")
            match_list.append(rows)
        elif word in rows['data']["telefonos"][0]:
            print("Encontrado")
            match_list.append(rows)
        elif word in rows['data']["ips"]:
            print("Encontrado")
            match_list.append(rows)
        elif word in rows['data']["email"]:
            print("Encontrado")
            match_list.append(rows)
        elif word in rows['data']["webs"]:
            print("Encontrado")
            match_list.append(rows)
        else:
            custom_regexp = re.compile( create_custom_regex(word))
            results = custom_regexp.findall(rows['text'])
            if len(results)>0:
                match_list.append(rows)

    return match_list


def insert_user_actions(chat_id, action):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_CREDITS_COLLECTION]
    row = {'chat_id': chat_id, 'time_insert':  get_time_stamp(), 'action':action}
    mycollection.insert_one(row)


def get_user_actions(chat_id):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_CREDITS_COLLECTION]
    myquerysend = {"chat_id": chat_id,'action':'upload'}
    myquerysearch = {"chat_id": chat_id, 'action': 'search'}
    mydocsend = mycollection.find(myquerysend)
    mydocsearch = mycollection.find(myquerysearch)

    send = len(list(mydocsend))
    search = len(list(mydocsearch))

    return send,search

def get_user_subscription(chat_id):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_PAY_COLLECTION]
    query = {"chat_id": chat_id, 'status': 'ok'}
    doc = mycollection.find(query)
    if len(list(doc)) == 0:
        return False
    else:
        return True

def insert_user_payment(chat_id, status):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_PAY_COLLECTION]
    row= {"chat_id":chat_id,"time_pay": get_time_stamp(),"status":status}
    mycollection.insert_one(row)

def get_user_paytime(chat_id):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_PAY_COLLECTION]
    query = {"chat_id": chat_id}
    doc = mycollection.find(query)
    find_data = ''
    for data in doc:
        print(data)
        if find_data in data['time_pay']:
            print("Encontrado")
            find_data = data['time_pay']
            return find_data




# Subir
def insert_user_permissions(chat_id, send_images_permission, search_images_permissions):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_PERMISSIONS_COLLECTION]
    row = {"chat_id": chat_id, "send_images_permission": send_images_permission, 'search_images_permissions':search_images_permissions}
    mycollection.insert_one(row)

def get_user_send_images_permission(chat_id):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_PERMISSIONS_COLLECTION]
    query = {"chat_id": chat_id, 'send_images_permission': 1}
    doc = mycollection.find(query)
    if len(list(doc)) == 0:
        return False
    else:
        return True

def update_user_send_images_permission(chat_id,user_send_images_permission):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_PERMISSIONS_COLLECTION]
    myquery = {"chat_id": chat_id}
    newvalues = {"$set": {'send_images_permission': user_send_images_permission}}
    mycollection.update_one(myquery, newvalues)

# Buscar
def get_user_search_images_permission(chat_id):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_PERMISSIONS_COLLECTION]
    query = {"chat_id": chat_id, 'search_images_permissions': 1}
    doc = mycollection.find(query)
    if len(list(doc)) == 0:
        return False
    else:
        return True

def update_user_search_images_permission(chat_id,search_images_permissions):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_PERMISSIONS_COLLECTION]
    myquery = {"chat_id": chat_id}
    newvalues = {"$set": {'send_images_permission': search_images_permissions}}
    mycollection.update_one(myquery, newvalues)

def get_subscribed_users():
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_PAY_COLLECTION]
    myquery = {"status": "ok"}
    doc = mycollection.count_documents(myquery)
    return doc

def get_user_uploaded_images():
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_CREDITS_COLLECTION]
    myquery = [{"$unwind": "$chat_id"},{"$group": {"_id": "$chat_id", "count": {"$sum": 1}}}]
    doc = list(mycollection.aggregate(myquery))
    return doc


def get_number_of_images_in_database():
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_IMAGE_COLLECTION]
    doc = mycollection.count_documents({})
    return doc

def get_number_of_searches():
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_U_CREDITS_COLLECTION]
    myquery = {"action": "search"}
    doc = mycollection.count_documents(myquery)
    return doc