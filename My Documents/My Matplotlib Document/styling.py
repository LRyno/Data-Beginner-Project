import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

# https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
# https://matplotlib.org/stable/users/explain/customizing.html

style.use('ggplot')

langs = ['Pyrhon', 'C++', 'Java', 'C#', 'Go']
votes = [50,24,14,6,17]
explodes = [0,0,0,0.2,0]

plt.pie(votes, labels=None, explode=explodes,
        autopct='%.2f%%', pctdistance=0.7, startangle=90)
plt.legend(labels=langs)

plt.show()