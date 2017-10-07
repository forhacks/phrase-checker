from gensim.models.word2vec import *
import numpy as np
import re

# hyperparams
max_len = 25
word2vec_size = 300
input_size = max_len * word2vec_size * 2
epochs = 1000
learning_rate = 0.000001


def process_def(definition):
    if len(definition) == 1:
        return definition
    definition = re.sub("[^a-zA-Z\s]", " ", definition)
    def_arr = np.array(definition.split(), dtype="S15")
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

# reorganize into [[def 1, def 2, 1/0], [def 1, def 2, 1/0], ...]
data = np.reshape(data, (-1, 3))

x = data[:len(data)]
y = np.array([map(int, data.T[len(data[0])-1])])

model = Word2Vec.load("word2vec model/trained/trained.w2v")

x = [[model.wv[word] for word in a] for a in x]
x = np.array([np.append(a[0], a[1]) for a in x])

# init weights and the bias
w = np.zeros((1, input_size))
b = 0


def sigmoid(f_a):
    return 1 / (1 + np.exp(-f_a))


print '-- STARTING TRAINING --'

for i in range(epochs):
    # init loss
    j = 0

    # multiply inputs by weights and and bias
    z = x.dot(w.transpose()) + b

    # take sigmoid
    a = sigmoid(z)
    # calculate the loss
    j += -np.sum(np.dot(y, np.log(a)) + np.dot(1 - y, np.log(1 - a))) / len(x)

    # derivative of z
    dz = a - y

    # update w and b
    w -= learning_rate * (np.sum(np.dot(dz, x), axis=0) / len(x))
    b -= learning_rate * np.sum(dz) / len(x)

    # print loss
    print "Loss: " + str(j)

print
print '-- STARTING TESTING --'
print

# repeat above steps for test data
test_x = x

test_y = y

z = x.dot(w.transpose()) + b
a = sigmoid(z)

print(a)
print(y)
