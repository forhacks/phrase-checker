from gensim.models.word2vec import *
import numpy as np

# hyperparams
max_len = 25


def process_def(definition):
    if len(definition) == 1:
        return definition
    def_arr = np.array(definition.split(), dtype="S75")
    word_count = len(def_arr)
    stretch = ([max_len/word_count + 1] * (max_len % word_count))
    stretch.extend([max_len/word_count] * (word_count - max_len % word_count))
    def_arr = np.repeat(def_arr, stretch)
    return def_arr


# read in defs
with open("definitions.txt") as f:
    data = f.readlines()

# remove \n at end
data = [process_def(x.strip()) for x in data]

data = np.reshape(data, (-1, 3)).T

x = data[:2]
y = map(int, data[2:][0])

print(x)

