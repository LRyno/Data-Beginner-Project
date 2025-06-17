import numpy as np
import matplotlib.pyplot as plt

x = ['C++', 'C#', 'Python', 'Java', 'Go']
y = [20, 50, 140, 1, 45]

plt.bar(x, y, color='r', align='edge', width=0.5, edgecolor='black', lw=3)
plt.xlabel('Program Language')
plt.ylabel('People')
plt.show()