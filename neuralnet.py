from gensim.models.word2vec import *
import numpy as np
import re

# hyperparams
max_len = 25
word2vec_size = 300
input_size = max_len * word2vec_size * 2
epochs = 100
learning_rate = 0.0000005


def process_def(definition):
    if len(definition) == 1:
        return definition
    definition = re.sub("[^a-zA-Z\s]", " ", definition).split()
    definition = [a for a in definition if len(a) > 2]
    def_arr = np.array(definition, dtype="S15")
    word_count = len(def_arr)
    stretch = ([max_len/word_count + 1] * (max_len % word_count))
    stretch.extend([max_len/word_count] * (word_count - max_len % word_count))
    def_arr = np.repeat(def_arr, stretch)
    return def_arr

print '-- READING DATA --'

# read in defs
with open("definitions.txt") as f:
    data = f.readlines()

# remove \n at end
data = [process_def(x.strip()) for x in data]

# reorganize into [[def 1, def 2, 1/0], [def 1, def 2, 1/0], ...]
data = np.reshape(data, (-1, 3)).T

x = data[:2].T
y = np.array([map(int, data[2:][0])])

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
    print "\r" + str(i) + "/" + str(epochs) + \
          " [" + ("#" * ((i * 10) / epochs)) + ("." * (10 - ((i * 10) / epochs))) + \
          "] Loss: " + str(j),

print
print '-- STARTING TESTING --'
print

# repeat above steps for test data
test_x = x

test_y = y

z = test_x.dot(w.transpose()) + b
a = sigmoid(z)

print(a)
print(test_y)

print
print 'Author Inputted Definitions'
print

def1 = "cats"
def2 = "being guided by what is right"

test_x = [[process_def(def1)], [process_def(def2)]]
test_x = [[model.wv[word] for word in a] for a in test_x]
test_x = np.append(test_x[0], test_x[1])

z = test_x.dot(w.transpose()) + b
a = sigmoid(z)

print(a)
