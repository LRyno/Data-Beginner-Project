import numpy as np
import matplotlib.pyplot as plt

x1, y1 = np.random.random(100), np.random.random(100)
x2, y2 = np.arange(100), np.random.random(100)

# Dalam beda window
# plt.figure(1)
# plt.scatter(x1,y1)

# plt.figure(2)
# plt.plot(x2,y2)

# plt.show()


# Dalam 1 window
# figure 1
fig = plt.figure()

years = [2006 + x for x in range(16)]
weights = [80, 83, 84, 85, 86, 82, 81, 79, 83, 80, 82, 82, 83, 81, 80, 79]

axs1 = fig.add_subplot(2,2,1)
axs1.plot(years,weights, c='r', lw='5', linestyle='--')
axs1.set_xlabel('Years')
axs1.set_ylabel('Weights')
axs1.set_title('Yearly Heights')

# figure 2
x = ['C++', 'C#', 'Python', 'Java', 'Go']
y = [20, 50, 140, 1, 45]

axs2 = fig.add_subplot(2,2,2)
axs2.bar(x, y, color='r', align='edge', width=0.5, edgecolor='black', lw=3)
axs2.set_xlabel('Program Language')
axs2.set_ylabel('People')
axs2.set_title('Program language users')

# figure 3
heights = np.random.normal(172,8,300)

axs3 = fig.add_subplot(2,2,3)
axs3.boxplot(heights)
axs3.set_xlabel('test')
axs3.set_ylabel('testing')
axs3.set_title('Tester')

# figure 4
x_data = np.random.random(50) * 100
y_data = np.random.random(50) * 100

axs4 = fig.add_subplot(2,2,4)
axs4.scatter(x_data, y_data, c='red', s=100)
axs4.set_title('Scatter plot')

plt.subplots_adjust(hspace=0.5, wspace=0.3)
fig.suptitle('Fourth Plot')

plt.show()
# plt.savefig('fourplots.png', dpi=500, transparent=False)