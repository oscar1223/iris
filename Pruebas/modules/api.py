import json

from bson import json_util
from flask import Flask, abort
from flask_restful import Api, Resource, reqparse

from modules.query import find_words, get_user_uploaded_images, get_subscribed_users, \
    get_number_of_images_in_database, get_number_of_searches

app = Flask(__name__)
api = Api(app)

words = {}

def abort_if_dosnt_find_word():
    abort(404, message="Ha habido un problema")

def parse_json(data):
    return json.loads(json_util.dumps(data))

class Search(Resource):
    def get(self,word):
        images_list=[]
        for row in find_words(word):
            data = parse_json(row)
            images_list.append(data)
        return {"data":images_list}

    def post(self):
        return {"Hello world":"Posted"}

class Count(Resource):
    def get(self):
        return {"Number of acitve licenses": get_subscribed_users(),
               "Number of images each user has uploaded": get_user_uploaded_images(),
                "Number of images in the database": get_number_of_images_in_database(),
                "Number of searches made by users": get_number_of_searches()
                }


api.add_resource(Search,"/search/<string:word>")
api.add_resource(Count,"/count")

if __name__ == "__main__":
    app.run(debug=True)