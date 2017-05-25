import matplotlib.pyplot as plt
import numpy as np

n_rows = 5
n_cols = 5
positions = [1,3]

board = np.zeros((n_rows,n_cols,3))

fig = plt.figure(figsize=[n_rows, n_cols])

# ax = fig.add_subplot(111)
ax = board.add_subplot(111)
ax.set_position([0,0,1,1])

for x in range(n_rows+1):
    ax.plot([x,x],[0,n_rows],'k')
for y in range(n_cols+1):
    ax.plot([0,n_cols],[y,y],'k')


# ax.imshow(fig, interpolation='nearest')
plt.show()
