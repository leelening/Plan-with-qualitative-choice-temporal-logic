import json
from this import s
from wdfa.helpers import check_dir
from mdp.mdp import MDP
from solver.lp_solver import LPSolver
from collections import defaultdict
from utils import plot_heatmap, save_trajectories
from simulation.simulator import Simulator
import yaml

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

for a in mdp.actions:
    for ns in mdp.transitions[1, 0][a]:
        mdp.transitions[1, 0][a][ns] = 0
    mdp.transitions[1, 0][a][1, 0] = 1

solver = LPSolver(mdp, path=prefix, disp=False)

solver.solve()


plot_heatmap(mdp.grid_world_size, solver.value)


simulator = Simulator(mdp=mdp, policy=solver.policy, target=(1, 0))

sampled_trajectories = simulator.sample_trajectories(10)

save_trajectories(sampled_trajectories=sampled_trajectories, prefix=prefix)
