import matplotlib.pyplot as plt
import numpy as np

board = np.zeros((4,4,3))
board += 0.5
board[::2, ::2] = 1
board[1::2, 1::2] = 1

# Obstaculos
positions = [1,3]

fig, ax = plt.subplots()
ax.imshow(board, interpolation='nearest')

queen = plt.imread('queen.png')
extent = np.array([-0.4, 0.4, -0.4, 0.4])
for y,x in enumerate(positions):
    ax.imshow(queen, extent=extent + [x,x,y,y])

ax.set(xticks=[], yticks=[])
ax.axis('image')

plt.show()

print board
