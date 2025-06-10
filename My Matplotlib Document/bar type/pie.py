import numpy as np
import matplotlib.pyplot as plt

langs = ['Pyrhon', 'C++', 'Java', 'C#', 'Go']
votes = [50,24,14,6,17]
explodes = [0,0,0,0.2,0]

plt.pie(votes, labels=None, explode=explodes,
        autopct='%.2f%%', pctdistance=0.7, startangle=90)
plt.legend(labels=langs)

plt.show()