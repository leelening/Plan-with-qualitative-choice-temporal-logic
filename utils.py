import os
from matplotlib import cm
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
from itertools import product


def check_existence(prefix):
    path = os.path.join("./", prefix)
    if not os.path.exists(path):
        os.makedirs(path)


def to_number(x, y):
    return 4 * (3 - y) + x


def dx_dy(a):
    if a == 0:
        dx, dy = 0, 0.2
    elif a == 1:
        dx, dy = 0.2, 0
    elif a == 2:
        dx, dy = 0, -0.2
    elif a == 3:
        dx, dy = -0.2, 0
    return dx, dy


def visualize_value(df, q):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(0, 4)
    Y = np.arange(0, 4)
    Z = np.zeros((4, 4))
    for x, y in product(range(4), repeat=2):
        state = (to_number(x, y), q)
        index = df["state"] == state
        Z[x][y] = df.loc[index]["value"].values[0]
    X, Y = np.meshgrid(X, Y)
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    # Customize the z axis.

    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


def visualize_policy(df, q):
    x = np.linspace(0, 4, 5)
    y = np.linspace(0, 4, 5)

    pl.figure(figsize=(10, 10))

    hlines = np.column_stack(np.broadcast_arrays(x[0], y, x[-1], y))
    vlines = np.column_stack(np.broadcast_arrays(x, y[0], x, y[-1]))
    lines = np.concatenate([hlines, vlines]).reshape(-1, 2, 2)
    line_collection = LineCollection(lines, color="black", linewidths=1)
    ax = pl.gca()
    ax.add_collection(line_collection)
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(y[0], y[-1])
    ax.set_xticks(x)
    ax.set_yticks(y)

    for x, y in product(range(4), repeat=2):
        state = (to_number(x, y), q)
        index = df["state"] == state
        action = df.loc[index]["policy"].values[0]
        dx, dy = dx_dy(action)
        plt.arrow(x + 0.5, y + 0.5, dx, dy, head_width=0.05)

    rect1 = patches.Rectangle(
        (0, 3), 1, 1, linewidth=1, edgecolor="grey", facecolor="grey"
    )
    rect2 = patches.Rectangle(
        (1, 2), 1, 1, linewidth=1, edgecolor="grey", facecolor="grey"
    )

    rect3 = patches.Rectangle(
        (1, 1), 1, 1, linewidth=1, edgecolor="grey", facecolor="grey"
    )
    rect4 = patches.Rectangle(
        (3, 0), 1, 1, linewidth=1, edgecolor="grey", facecolor="grey"
    )

    ax.add_patch(rect1)
    ax.add_patch(rect2)
    ax.add_patch(rect3)
    ax.add_patch(rect4)
    plt.show()
