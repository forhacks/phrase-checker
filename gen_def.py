# encoding: utf-8

# TODO:
# do words that are not same
# save in array.

import requests, time, random
from xml.etree import ElementTree
from multiprocessing import Pool

ox_id = "83a8d0b7"  # ENTER_OX_APP_ID
ox_key = "a41bec7e5a3e6d9f7f3e738498d42def"  # ENTER_OX_APP_KEY
mw_key = "90cecf59-d31f-4c48-9286-ee48d249bdcb"  # ENTER_MW_THESAURUS_KEY

assert ox_id != ""
assert ox_key != ""
assert mw_key != ""

headers = {
    "Accept": "application/json",
    "app_id": ox_id,
    "app_key": ox_key
}

word_file = open("words.txt", "r")
word_list1 = word_file.read().split()
word_list2 = list(word_list1)

random.shuffle(word_list1)
random.shuffle(word_list2)

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


def get_pair(i):

    ox_word = word_list1[i]
    mw_word = word_list2[i]

    try:

        ox_def = get_ox_def(ox_word)
        mw_def = get_mw_def(mw_word)

        print(ox_def, mw_def)

        if ox_def is not None and mw_def is not None:
            return ox_def, mw_def

    except Exception:
        return None


p = Pool()

out = open('gen_def.txt', 'a')
interval = 5

for i in range(0, 5000, interval):

    print('Starting words', i+1, '-', i+interval)
    a = [x for x in p.map(get_pair, range(i, i+interval)) if x is not None]
    tries = 0

    while len(a) == 0 and tries <= 4:
        print('Received no results. Retrying...')
        time.sleep(20)
        a = [x for x in p.map(get_pair, range(i, i+interval)) if x is not None]
        tries += 1
    if tries == 4:
        print('Continuing after 4 tries.')

    out.write('\n'.join('\n'.join(x + ('1',)) for x in a))
    out.write('\n')
    print('Finished words', i+1, '-', i+interval, 'with', len(a), 'results')
    print

out.close()
