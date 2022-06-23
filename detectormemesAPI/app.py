import zlib

from flask import Flask, request

from modules.mongo import find_words

app = Flask(__name__)


@app.route('/images')
def hello_world():
    word = request.args.get('word', default="", type=str)
    source = request.args.get('source', default="", type=str)
    img_dict={}
    count = 0
    for img in find_words(word,source):
        img1 = zlib.decompress(img)
        decode = img1.decode()
        img_dict[count] = decode
        count +=1
    return img_dict


if __name__ == '__main__':
    app.run()
