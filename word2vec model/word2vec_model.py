from gensim.models.word2vec import *
import multiprocessing
import os

model = None
if not os.path.exists("trained/trained.w2v"):
    print "Training"
    sentences = LineSentence("data/text.txt")
    model = Word2Vec(sentences, size=300, min_count=10, workers=multiprocessing.cpu_count(), iter=10)
    model.save("trained/trained.w2v")
else:
    print "Loading"
    model = Word2Vec.load("trained/trained.w2v")

print model.wv.similarity("fact", "truth")
print model.wv.similarity("fact", "lie")
