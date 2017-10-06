import pandas as pd
import numpy as np
import string

data = np.array(pd.read_csv("data/articles1.csv").as_matrix())
data = data.T[8:][1:]
data = data.reshape((len(data[0]),))
text = string.join(data)
text = text.replace(",", "")
text = " ".join(text.split())

f = open('data/text.txt', 'w')
f.write(text)
f.close()
