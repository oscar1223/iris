from bots.Redditbot import start_reddit_bot
from bots.instaDownloader import get_username_from_txt
from bots.twitterbot import start_twitter_bot
from bots.telegrambot import innit_bot
from modules.imageProcessing import console_input
from modules.var_c import TXT_INSTAGRAM_USERS

if __name__ == "__main__":
    print("Seleccione una opcion:\n\t1)Introduccion de datos en masa \n\t2)Bot de telegram\n\t3)Bot de instagram\n\t4)Bot de reddit\n\t5)Bo de Twitter")
    value = input()
    if value == "1":
        console_input()
    elif value == "2":
        innit_bot()
        print('==== BOT DE TELEGRAM ACTIVADO ====')
    elif value == "3":
        get_username_from_txt(TXT_INSTAGRAM_USERS)
    elif value == "4":
        start_reddit_bot()
    elif value == "5":
        start_twitter_bot()
    else:
        print("Seleccione una opcion valida")

