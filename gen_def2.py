# encoding: utf-8

import requests


def get_wapi_text(word):

    url = "https://wordsapiv1.p.mashape.com/words/" + word + "/definitions"
    r = requests.get(url)

    print r.status_code

    try:
        j = r.json()
    except ValueError:
        return None

    print j

get_wapi_text("word")
