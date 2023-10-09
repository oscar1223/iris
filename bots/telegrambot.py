###
# Bot de Telegram con el cual el usuario puede recuperar fotos
# de nuestra base de datos con información que le resulte importante
# la cual tiene que ser pagada mediante la subida de fotos a nuestra base de datos
# Telegram bot that uploads images to the database and queries it searching for
# names, ips, phone numbers, web addresses and established names
# ###

from datetime import datetime
import telebot
from telebot.types import LabeledPrice
from modules import var_c
from modules.er import beautify_fecha, beatify_text_search, source_clasifier
from modules.compress import return_image_from_bson, decompressBson
from modules.imageProcessing import data_processing, image_write
from modules.query import find_words, insert_user_actions, get_user_actions, get_user_subscription, insert_user_payment, insert_user_permissions, get_user_send_images_permission, update_user_send_images_permission, get_user_search_images_permission, update_user_search_images_permission, get_user_paytime
from modules.texts import NUMBER_OF_CREDITS
from modules.var_c import ROUTE_IMAGE_DIRECTORY, FREE_TRIAL
from modules import texts


TOKEN = var_c.TOKEN
ABOUT_TEXT = texts.ABOUT_TEXT

bot = telebot.TeleBot(TOKEN, threaded=True)

prices = [LabeledPrice(label='Dantes Gates OCR Monitor', amount=999)]

# Start method
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    insert_user_permissions(message.chat.id, 0, 0)
    bot.reply_to(message, ABOUT_TEXT)

# Upload method
@bot.message_handler(commands=['subir'])
def upload(message):
    update_user_send_images_permission(message.chat.id, user_send_images_permission=1)
    bot.reply_to(message, 'Suba una foto')

# Subscribe method
@bot.message_handler(commands=['suscribete'])
def subscribe(message):
   bot.send_message(message.chat.id,
                    texts.INVOICE_TEXT
                    , parse_mode='Markdown')
   bot.send_invoice(message.chat.id,
                    title=texts.TITLE,
                    description = texts.DESCRIPTION,
                    provider_token = var_c.STRIPE_PRODUCTION_KEY,
                    currency=texts.CURRENCY,
                    photo_url='https://i.imgur.com/1apJYI0.png',
                    photo_height=512,
                    photo_width=512,
                    photo_size=512,
                    is_flexible=False,
                    prices=prices,
                    start_parameter='dg-ocr-service',
                    invoice_payload="Custom-Payload"
   )


# Checkout method before pay.
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message=texts.CHECKOUT_ERROR)


#Payment method
@bot.message_handler(content_types='successful_payment')
def got_payment(message):
    bot.send_message(message.chat.id,
                     texts.GOT_PAYMENT.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')
    insert_user_payment(message.chat.id, 'ok')


# Search method
@bot.message_handler(commands=['buscar'])
def search(message):

    send, search = get_user_actions(message.chat.id)
    if (send-search) > 0 & get_user_search_images_permission(message.chat.id):
        try:
            now = datetime.today()
            date_now = datetime.strptime(now.strftime('%d/%m/%Y'), '%d/%m/%Y')

            pay_time = datetime.strptime(
                datetime.strftime(datetime.strptime(get_user_paytime(message.chat.id), '%d/%m/%Y, %H:%M:%S'), '%d/%m/%Y'),
                '%d/%m/%Y')

            different_dates = (date_now - pay_time).days

            rest_date = 365 - int(different_dates)
            bot.reply_to(message, f'Te quedan {rest_date} dias para que se acabe tu suscripcion.')
        except:
            bot.reply_to(message, f'Considera suscribirte a nuestro servicio, tenemos una oferta de lanzamiento del 80%!!')
        bot.reply_to(message, NUMBER_OF_CREDITS.format({send-search}))

        bot.reply_to(message,texts.SEARCH_WORD)

    else:
        bot.reply_to(message, texts.NO_CREDIT)
    update_user_search_images_permission(message.chat.id, 1)

# Change the boolean state to search
@bot.message_handler(func=lambda message:True)
def echo_all(message):
    update_user_search_images_permission(message.chat.id, 0)
    send_user_search_query(message)


# Function to search word.
def send_user_search_query(message):
    word = message.text
    source = ''
    match_insta = []
    match_reddit = []
    match_twitter = []
    match_telegram = []
    matches = find_words(word.upper())

    if len(list(matches)) != 0:
        insert_user_actions(message.chat.id, 'search')
        for i in matches:
            if source_clasifier(source) == 'instagram':
                match_insta.append(i)
            elif source_clasifier(source) == 'reddit':
                match_reddit.append(i)
            elif source_clasifier(source) == 'twitter':
                match_twitter.append(i)
            else:
                match_telegram.append(i)

        bot.reply_to(message, f'Se han encontrado {len(list(match_insta))} imágenes en Instagram\n'
                              f'Se han encontrado {len(list(match_reddit))} imágenes en Reddit\n'
                              f'Se han encontrado {len(list(match_twitter))} imágenes en Twitter\n'
                              f'Se han encontrado {len(list(match_telegram))} imágenes subidas por usuarios')
      
        if FREE_TRIAL:
            for match in matches:
                #bot.reply_to(message, beatify_text_search(match))
                bot.send_photo(chat_id=message.chat.id, photo=return_image_from_bson(decompressBson(match['image'])),
                               caption="Imagen encontrada")
        else:
            if get_user_subscription(message.chat.id):
                for match in matches:
                    bot.reply_to(message, beatify_text_search(match))
                    bot.send_photo(chat_id=message.chat.id, photo=return_image_from_bson(decompressBson(match['image'])),
                                   caption="Imagen encontrada")
            else:
                bot.reply_to(message, texts.SUBSCRIBE)
    else:
        bot.reply_to(message, texts.NO_FOUND_PHOTO)


# Method that downloads the image and sends it to the database
def processPhotoMessage(message):
    if get_user_send_images_permission(message.chat.id):
        update_user_send_images_permission(message.chat.id, 0)
        print('message.photo =', message.photo)
        fileID = message.photo[-1].file_id
        print('fileID =', fileID)
        file = bot.get_file(fileID)
        print('file.file_path =', file.file_path)
        downloaded_file = bot.download_file(file.file_path)
        fecha = beautify_fecha()
        image_write(downloaded_file, fecha, message)
        name = message.chat.id
        try:
            texto_final = data_processing(name, ROUTE_IMAGE_DIRECTORY + "temp_image.jpg")
            bot.reply_to(message, "Procesando...")
            bot.reply_to(message, texto_final)
            insert_user_actions(name, 'upload')
        except:
            bot.reply_to(message, 'Imagen Invalida')

    else:
        bot.reply_to(message, texts.UPLOAD_IMAGE)


@bot.message_handler(content_types=['photo'])
def photo(message):
    processPhotoMessage(message)

def invalid_image(message):
    bot.reply_to(message, 'Imagen invalida')


def innit_bot():
   bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
   innit_bot()

    
