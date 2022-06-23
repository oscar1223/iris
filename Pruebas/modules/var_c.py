import sys

# Tesseract-OCR path
path_tesseract = '/usr/share/tesseract-ocr/tessdata'
# Configuración de Terreract-OCR, para más información consultar la documentación
custom_config = r"--oem 3 --psm 11 -c tessedit_char_whitelist= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '"

# irectorio en el que se guardarán las imágenesD
memes_directory = "memes/*"


# Date format
date_format = "%d/%m/%Y, %H:%M:%S"

# Spanish phone regExp
reg_exp_phone_spain = r"(?:(?:\+(?:[0]{0,4})?)?34[. -]{0,3})?[6789][0-9]{2}[ ]{0,3}(?:[0-9][ ]?){5}[0-9]"
# International phone regExp
reg_exp_phone_international = r"\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}"
# web address regExp
reg_exp_web = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
# ip regExp
reg_exp_ip = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
# Garbage characters regExp
reg_exp_garbage_characters = r"([A-Z])\w+|([0-9])\w+/gi"
# Source regExp
reg_exp_instagram = r"/(Instagram)?(instagram)?/g"
reg_exp_reddit = r"/(Reddit)?(reddit)?/g"
reg_exp_twitter = r"/(Twitter)?(twitter)?/g"



# Importat words dictionary
names_dictionary = {
    'putin': 1,
    'biden': 2,
    'trump': 3,
    'broncano': 4
}

#Names csv

CSV_SPANISH_MALE_NAMES= "hombres.csv"
CSV_SPANISH_FEMALE_NAMES= "mujeres.csv"
CSV_SPANISH_LASTNAMES= "apellidos.csv"



# Información de la cadena de conexión a la base de datos
conection_string = {
    "database": "postgres",
    "user": "postgres",
    "password": "root",
    "host": "127.0.0.1",
    "port": "5432"
}


#Bot Father token.
TOKEN = '5057433468:AAE941tjm5IAyi6MYsPukrmMQZNPpF9whrI'
STRIPE_PRODUCTION_KEY = '350862534:LIVE:NjJkOTg3YWYwZTM1'


# Ruta absoluta de la carpeta que contendrá las imágenes descargadas
ROUTE_IMAGE_DIRECTORY = sys.path[0]+"/memes/"


# Instagram login
INSTA_USER = 'pacaadmin1234'
INSTA_PASSWD = 'admin1234$A'


# Instagram username list
TXT_INSTAGRAM_USERS = "cuentasmemesInstagram"


#MongoDB strings
MONGO_DATABASE_NAME = 'imagenes'
MONGO_IP = "mongodb://localhost:27017/"

# Images database collection
MONGO_IMAGE_COLLECTION = 'imagenes'

# U_CREDITS database collection
MONGO_U_CREDITS_COLLECTION = 'u_credits'

# Payments database collection
MONGO_U_PAY_COLLECTION = 'u_pay'

# Permissions database collection
MONGO_U_PERMISSIONS_COLLECTION = 'u_permissions'

# Redit credentials
REDDIT_CLIENT_ID = 'XJb5kGjeNIWRft-ns4b-ww'
REDDIT_SECRET = 'UODYfh9FRQeK4-kCeUogJDrLPVRYUg'
REDDIT_USER_AGENT = "<GetImageBot>"

# Variable that controls if an user has to pay
FREE_TRIAL = True

# TWITTER KEYS AND API TOKENS
TWT_consumer_key = 'yKnhwGcg7HTNHKykQOrIJKIeY'
TWT_consumer_secret = 'nN7V6fVHxZMACkKX8l1xfBEDudTR9YtS9gib7KtGt1timKs5ZE'
TWT_access_token = '729613355871285248-PtEMZZ5dK6mmLzEysRUfqA3SRbNhMkQ'
TWT_access_token_secret = 'W4v5LHD32xmHY0WzVrjAbFYYSZK0Rf1YcNHMng7AihC53'