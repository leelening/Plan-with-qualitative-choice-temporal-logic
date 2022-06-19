from this import s
from wdfa.helpers import check_dir
from mdp.mdp import MDP
from solver.lp_solver import LPSolver
from collections import defaultdict
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

prefix = "mdp_example"

check_dir(prefix)


mdp = MDP(
    file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"
)


mdp.reward = defaultdict(float)
mdp.reward[(2, 0), 3] = 1
mdp.reward[(1, 1), 2] = 1
mdp.reward[(0, 0), 1] = 1
mdp.gamma = 0.9

for a in mdp.actlist:
    for ns in mdp.transitions[1, 0][a]:
        mdp.transitions[1, 0][a][ns] = 0

solver = LPSolver(mdp, path=prefix, print=False)

solver.solve()


res = np.zeros(solver.mdp.grid_world_size)
for (x, y), v in solver.value.items():
    if isinstance(x, int) and isinstance(y, int):
        res[x][y] = v

res = np.rot90(res)
ax = sns.heatmap(res)
yticks_pos = np.arange(0.5, 8.5, 1)
yticks_label = range(8)
plt.yticks(yticks_pos, yticks_label[::-1])
plt.show()
