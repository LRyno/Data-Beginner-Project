import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes(projection='3d')

# Scatter
# x = np.random.random(100)
# y = np.random.random(100)
# z = np.random.random(100)

# ax.scatter(x,y,z)

# Line
# x = np.arange(0,50,0.1)
# y = np.arange(0,50,0.1)
# z = np.cos(x+y)

# ax.plot(x,y,z)

# ax.set_title('3D Plot')
# ax.set_xlabel('test')
# ax.set_ylabel('tester')

# Area
x = np.arange(-5,5,0.1)
y = np.arange(-5,5,0.1)
X, Y = np.meshgrid(x,y)
Z = np.sin(X) * np.cos(Y)

ax.plot_surface(X,Y,Z, cmap='Spectral')
ax.set_title('3D Plot')
ax.set_xlabel('test')
ax.set_ylabel('tester')

plt.show()