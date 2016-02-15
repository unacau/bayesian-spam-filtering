import re

__author__ = 'Igor Ekishev'

REGEX_EMAIL = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
TOKENS = "abcdefghijklmnopqrstuvwxyz0123456789-$'"
WHITESPACE = '!()#%^&@*+}{][|/*":;.,<>?=\`~_'
REGEX_IP = '(?:[0-9]{1,3}\.){3}[0-9]{1,3}'
REGEX_HEX_COLOUR = '#(?:[0-9a-fA-F]{3}){1,2}'
REGEX_HTML = '<[^<]+?>'


def tokenize(body):
    # tokenize string, input string, output list of strings

    urls = extract_urls(body)
    list_of_colors = re.findall(REGEX_HEX_COLOUR, body)
    list_of_ips = re.findall(REGEX_IP, body)

    tokens = re.sub(REGEX_HTML, '', body) + urls  # remove html tags from text

    for el in WHITESPACE:
        tokens = tokens.translate(str.maketrans(el, ' '))  # clear text from 'noise'

    tokens = tokens.lower().split()
    tokens = remove_clear_ints(tokens)

    for el in list_of_ips:  # append IPs and HEX colours to tokens
        tokens.append(el)
    for el in list_of_colors:
        tokens.append(str.lower(el))

    return tokens


def extract_urls(text):
    urls = re.compile('(?i)<a([^>]+)>(.+?)</a>')
    list = urls.findall(text)
    sez = ''
    for i in list:
        for j in i:
            sez += j
    return sez


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def integers_in(list):
    for i in range(len(list)):
        if is_number(list[i]):
            return True
        else:
            False


def remove_clear_ints(tokens):
    while integers_in(tokens):
        for elements in tokens:
            if is_number(elements):
                tokens.remove(elements)
    return tokens
