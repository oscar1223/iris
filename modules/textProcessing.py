###
# Class that parsers the text of the images
# ###

import re

from stop_words import get_stop_words

from modules import er, var_c

# Searches ips in the text using regExp
from modules.var_c import CSV_SPANISH_MALE_NAMES, CSV_SPANISH_FEMALE_NAMES, CSV_SPANISH_LASTNAMES


def ip_processing(text):
    ips = []
    reg_exp_ip = var_c.reg_exp_ip
    for ip in text.split():
        if re.search(reg_exp_ip, ip):
            ips.append(ip)
    return ips


# Searches web addresses in the text using regExp
def web_processing(text):
    web = []
    reg_exp_web = var_c.reg_exp_web
    r = re.compile(reg_exp_web)
    results = r.findall(text)
    if results:
        for webs in results:
            print('|---------------[INFO][PARSER][WEB][>]: ' + str(webs))
            for elemento in webs:
                if elemento == "":
                    pass
                else:
                    web.append(elemento)

    return web


# Searches phone numbers in the text using regExp
def phone_processing(text):
    spain_phones = []
    internatinal_phones = []

    reg_exp_phone_spain = var_c.reg_exp_phone_spain
    reg_exp_phone_international = var_c.reg_exp_phone_international

    r_spain = re.compile(reg_exp_phone_spain)
    r_international = re.compile(reg_exp_phone_international)

    results_spain = r_spain.findall(text)
    resutls_international = r_international.findall(text)

    for telefono in results_spain:
        print('|---------------[INFO][PARSER][PHONE][SPAIN][>]: ' + str(telefono))
        spain_phones.append(telefono)

    for telefono in resutls_international:
        print('|---------------[INFO][PARSER][PHONE][INTERNATIONAL][>]: ' + str(telefono))
        internatinal_phones.append(telefono)

    return spain_phones, internatinal_phones


# Searches emails in the text using regExp
def email_processing(text):
    emails = []
    reg_exp_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    r_email = re.compile(reg_exp_email)
    results = r_email.findall(text)

    for email in results:
        email = er.replace_acentos(er.remove_tags(er.replace_non_english_characters(str(email))))
        print('|---------------[INFO][PARSER][EMAIL][>]: ' + str(email))
        emails.append(email)

    return emails


# Searches important words in the text using regExp
def names_processing(text):
    diccionario = var_c.names_dictionary
    names = []
    for nombre in text.split():
        cadena = nombre.lower()
        if cadena in diccionario:
            names.append(nombre)

    return names


def parseMAIN(text):
    names = [get_spanish_names(text),get_spanish_last_names(text)]
    email = email_processing(text)
    phone_numbers = phone_processing(text)
    ips = ip_processing(text)
    webs = web_processing(text)
    data = {
        'nombres': names,
        'email': email,
        'telefonos': phone_numbers,
        'ips': ips,
        'webs': webs
    }
    return data


def get_spanish_names(text):
    stop_words = get_stop_words('spanish')
    names = []

    with open(CSV_SPANISH_MALE_NAMES) as fp:
        male_names = fp.read()
    with open(CSV_SPANISH_FEMALE_NAMES) as fp:
        female_names = fp.read()

    for word in text.split():
        lower_word = word.lower()
        if not lower_word in stop_words:
            if word.upper() in male_names:
                names.append(word)
            if word.upper() in female_names:
                names.append(word)

    return names


def get_spanish_last_names(text):
    stop_words = get_stop_words('spanish')
    last_names = []

    with open(CSV_SPANISH_LASTNAMES) as fp:
        last_names_csv = fp.read()

    for word in text.split():
        lower_word = word.lower()
        if not lower_word in stop_words:
            if word.upper() in last_names_csv:
                last_names.append(word)

    return last_names

