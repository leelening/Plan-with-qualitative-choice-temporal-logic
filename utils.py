import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from itertools import product


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
