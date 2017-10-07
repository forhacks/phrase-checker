# encoding: utf-8

import requests, time
from xml.etree import ElementTree
from multiprocessing import Pool

ox_id = ""  # ENTER_OX_APP_ID
ox_key = ""  # ENTER_OX_APP_KEY
mw_key = ""  # ENTER_MW_THESAURUS_KEY

assert ox_id != ""
assert ox_key != ""
assert mw_key != ""

headers = {
    "Accept": "application/json",
    "app_id": ox_id,
    "app_key": ox_key
}

word_file = open("words.txt", "r")
word_list = word_file.read().split()
word_file.close()


def get_ox_def(f_word):

    url = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/" + f_word

    r = requests.get(url, headers=headers)

    try:
        j = r.json()
    except ValueError:
        return None

    return j["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0].replace(u"–", "-")


def get_mw_def(f_word):

    url = "http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/" + f_word + "?key=" + mw_key

    r = requests.get(url)

    try:
        tree = ElementTree.fromstring(r.content)
        return tree.find('entry').find('sens').find('mc').text.replace(u"–", "-")
    except AttributeError:
        return None


def get_pair(word):

    try:

        ox_def = get_ox_def(word)
        mw_def = get_mw_def(word)

        if ox_def is not None and mw_def is not None:
            return ox_def, mw_def

    except Exception:
        return None


p = Pool()

out = open('gen_def.txt', 'a')
interval = 5

for i in range(1900, 5000, interval):

    print 'Starting words', i+1, '-', i+interval
    a = [x for x in p.map(get_pair, word_list[i:i+interval]) if x is not None]
    tries = 0

    while len(a) == 0 and tries <= 4:
        print 'Received no results. Retrying...'
        time.sleep(20)
        a = [x for x in p.map(get_pair, word_list[i:i+interval]) if x is not None]
        tries += 1
    if tries == 4:
        print 'Continuing after 4 tries.'

    out.write('\n'.join('\n'.join(x + ('1',)) for x in a))
    out.write('\n')
    print 'Finished words', i+1, '-', i+interval, 'with', len(a), 'results'
    print

out.close()
