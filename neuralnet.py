from gensim.models.word2vec import *
import numpy as np

# hyperparams
max_len = 25
epochs = 1000
learning_rate = 0.01


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

model = Word2Vec.load("word2vec model/trained/trained.w2v")

x = [[model.wv[word] for word in a] for a in x]
x = np.array([np.append(a[0], a[1]) for a in x])

# init weights and the bias
w = np.zeros((1, max_len))
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
    j += -np.sum(np.multiply(y, np.log(a)) + np.multiply(1 - y, np.log(1 - a))) / len(x)

    # derivative of z
    dz = a - y

    # update w and b
    w -= learning_rate * (np.sum(np.multiply(dz, x), axis=0) / len(x))
    b -= np.sum(dz) / len(x)

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
