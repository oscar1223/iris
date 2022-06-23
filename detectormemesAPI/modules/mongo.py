import re

from modules import var_c
import pymongo
from modules.er import create_custom_regex, source_clasifier
from modules.var_c import MONGO_U_CREDITS_COLLECTION, MONGO_IMAGE_COLLECTION, MONGO_IP, MONGO_DATABASE_NAME, \
    MONGO_U_PAY_COLLECTION, MONGO_U_PERMISSIONS_COLLECTION


# Search method
def find_words(word,source):
    CONNECTION_STRING = var_c.MONGO_DATABASE_NAME
    client = pymongo.MongoClient(MONGO_IP)
    mydb = client[CONNECTION_STRING]
    mycollection = mydb[MONGO_IMAGE_COLLECTION]
    print(f"Buscando palabra {word}")
    match_list = []

    for rows in mycollection.find():

        if word in rows['data']["nombres"][0]:
            print("Encontrado")
            match_list.append(rows["image"])
        elif word in rows['data']["nombres"][1]:
            print("Encontrado")
            match_list.append(rows["image"])
        elif word in rows['data']["telefonos"][0]:
            print("Encontrado")

            match_list.append(rows["image"])
        elif word in rows['data']["ips"]:
            print("Encontrado")
            match_list.append(rows["image"])
        elif word in rows['data']["email"]:
            print("Encontrado")
            match_list.append(rows["image"])
        elif word in rows['data']["webs"]:
            print("Encontrado")
            match_list.append(rows["image"])
        else:
            custom_regexp = re.compile(create_custom_regex(word))
            results = custom_regexp.findall(rows['text'])
            if len(results) > 0:
                match_list.append(rows["image"])


    return match_list
