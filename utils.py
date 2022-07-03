import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from itertools import product
import pandas as pd
from pandas import Series
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import rcParams


def plot_heatmap(size: list, value: dict):
    res = np.zeros(size)
    for (x, y), v in value.items():
        if isinstance(x, int) and isinstance(y, int):
            res[x][y] = v

    res = np.rot90(res)
    ax = sns.heatmap(res)
    yticks_pos = np.arange(0.5, size[1] + 0.5, 1)
    yticks_label = range(size[1])
    plt.yticks(yticks_pos, yticks_label[::-1])
    plt.show()


def plot_value_surf(size: list, value: dict, zlimit=None, title=None):
    plt.style.use("seaborn-dark")
    fig = plt.figure(figsize=(8, 8))

    ax = fig.gca(projection="3d")
    if title:
        fig.canvas.set_window_title(title)

    Z1 = np.zeros(size)

    X_VAL = np.arange(0, size[0], 1)
    Y_VAL = np.arange(0, size[1], 1)

    X1, Y1 = np.meshgrid(X_VAL, Y_VAL, sparse=False, indexing="ij")

    for (i, j) in product(X_VAL, Y_VAL):
        Z1[i][j] = value[i, j]

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Value")

    surf = ax.plot_surface(X1, Y1, Z1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))
    if zlimit:
        ax.set_zlim(0, zlimit)

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.dist = 12

    plt.show()


def return_error_on_initial_states(evaluator1, evaluator2):
    error = {}
    for k1, k2 in product(evaluator1.value, evaluator2.value):
        if (
            k1[0] == k2[0]
            and k1 != "sT"
            and k1[-1] == evaluator1.mdp._wdfa.initial_state
            and k2[-1] == evaluator2.mdp._wdfa.initial_state
        ):
            error[k1[0]] = evaluator1.value[k1] - evaluator2.value[k2]
    return error


def preprocess(row: Series):
    return eval(row["State"]) if row["State"] != "sT" else row["State"]


def read_policy(policy_path: str):
    df = pd.read_csv(policy_path, sep="\t")
    df["State"] = df.apply(preprocess, axis=1)
    policy = {}
    for _, row in df.iterrows():
        policy[row["State"]] = (
            int(row["Action"]) if row["Action"] != "aT" else row["Action"]
        )
    return policy


def save_trajectories(sampled_trajectories: list, prefix: str):
    with open("{}/trajectories.txt".format(prefix), "w") as f:
        for trajectory in sampled_trajectories:
            line = ", ".join(str(x) for x in trajectory)
            f.write("[" + line + "]\n")


def from_prob_to_cost(value: dict, weight: float, opt: float):
    cost = {}
    for s in value:
        if abs(value[s]) < 1e-4:
            cost[s] = opt + 1
        else:
            cost[s] = weight * value[s]
    return cost
