###
# This class contains all the necessary methods to beautify an string
# ###
import base64
import re
from datetime import datetime
from modules import var_c

# Method that returns the timestamp
from modules.var_c import reg_exp_garbage_characters, reg_exp_instagram, reg_exp_twitter, reg_exp_reddit


def get_time_stamp():
    now = datetime.now()
    date_time = now.strftime(var_c.date_format)
    return date_time


# Method that beautifys the timestamp
def beautify_fecha():
    date = get_time_stamp().replace(" ", "").replace("/", "-").replace(",", "_").replace(":", "-")
    return date


def beatify_text_search(lista):
    return f"Se ha encontrado la siguiente imagen: {lista['source']} con el texto: {lista['text']} y los datos relevantes: {lista['data']}"


# Method that returns the string
def replace_acentos(cadena):
    cadena = cadena.upper()
    cadena = cadena.replace('Á', 'A')
    cadena = cadena.replace('É', 'E')
    cadena = cadena.replace('Í', 'I')
    cadena = cadena.replace('Ó', 'O')
    cadena = cadena.replace('Ú', 'U')
    cadena = cadena.replace('Ñ', 'N')
    cadena = cadena.replace('Ä', 'A')
    cadena = cadena.replace('Ë', 'E')
    cadena = cadena.replace('Ï', 'I')
    cadena = cadena.replace('Ö', 'O')
    cadena = cadena.replace('Ü', 'U')
    return cadena.lower()


# Method that replaces non english characters
def replace_non_english_characters(cadena):
    cadena = cadena.upper()
    cadena = cadena.replace("Ñ", "N")
    return cadena.lower()


TAG_RE = re.compile(r'<[^>]+>')


# Method that deletes HTML tags
def remove_tags(text):
    return TAG_RE.sub('', text)


def get_garbage_characters(text):
    if re.search(reg_exp_garbage_characters, text):
        return True
    else:
        return False

def source_clasifier(source):

    if re.search(reg_exp_instagram, source):
        result = 'instagram'
    elif re.search(reg_exp_reddit, source):
        result = 'reddit'
    elif re.search(reg_exp_twitter, source):
        result = 'twitter'
    else:
        result = 'telegram'

    return result

def create_custom_regex(word):
    """\b([Dd][Oo][Gg])\b"""
    custom_regex = r"\b("
    for char in word:
        custom_regex += "["
        custom_regex += char.upper()
        custom_regex += char.lower()
        custom_regex += "]"
    custom_regex += r")\b"
    return custom_regex