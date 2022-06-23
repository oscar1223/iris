import re


from modules.var_c import reg_exp_garbage_characters, reg_exp_instagram, reg_exp_twitter, reg_exp_reddit

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