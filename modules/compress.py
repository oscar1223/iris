import base64
import zlib
import PIL
import bson
from bson.codec_options import CodecOptions
from PIL import Image

# Image compression method
def compressBson(imageBson):

    encodestr = zlib.compress(imageBson)

    return encodestr

# Image decompression method
def decompressBson(cimageBson):

    decodestr = zlib.decompress(cimageBson)

    return decodestr


# base64 encoding method
def image_to_base(image):
    with open(image, "rb") as image_file:
        Bson_image = base64.b64encode(image_file.read())

    return Bson_image


# base64 decoding method
def return_image_from_bson(image):
    with open('decoded_image.png', 'wb') as file_to_save:
        decoded_image_data = base64.decodebytes(image)
        file_to_save.write(decoded_image_data)
    return decoded_image_data



