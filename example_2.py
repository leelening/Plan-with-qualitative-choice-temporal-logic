from wdfa.helpers import get_wdfa_from_dfa, ordered_or, check_dir
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_2, DFA_8
from solver.lp_solver import LPSolver
from simulation.simulator import Simulator
from utils import save_trajectories, plot_value_surf, plot_heatmap
import os

prefix = "example_2"

check_dir(prefix)

wdfa2 = get_wdfa_from_dfa(DFA_2, path=prefix, name="F b")
wdfa8 = get_wdfa_from_dfa(DFA_8, path=prefix, name="F a | F c")

wdfa = ordered_or(wdfa2, wdfa8, path=prefix, name="F b OR (F a | F c)")

mdp = MDP(
    file_path="environment/8 x 8/1.yaml"
)

product_mdp = ProductMDP(mdp, wdfa)

solver = LPSolver(product_mdp, path=prefix, disp=False)

solver.solve()

value = {s[0]: solver.value[s] for s in product_mdp.states if s[-1] == ("0", "0")}
print(f"The value of the initial state (6, 6) for the F b OR (F a | F c): {value[6, 6]}")

# plot_value_surf(mdp.grid_world_size, value, path=os.path.join(prefix, "value surf.png"))
plot_heatmap(mdp.grid_world_size, value, path=os.path.join(prefix, "heatmap.png"))

# solve F b
product_mdp2 = ProductMDP(mdp, wdfa2)
solver2 = LPSolver(product_mdp2, path=os.path.join(prefix, "2"), disp=False)
solver2.solve()

value2 = {s[0]: solver2.value[s] for s in product_mdp2.states if s[-1] == "0"}
print(f"The value of the initial state (6, 6) for the F b: {value2[6, 6]}")
print(f"The value of the initial state (3, 0) for the F b: {value2[3, 0]}")
# plot_value_surf(mdp.grid_world_size, value2, path=os.path.join(prefix, "2", "value surf.png"))
plot_heatmap(mdp.grid_world_size, value2, path=os.path.join(prefix, "2", "heatmap.png"))

# solve F a | F c
product_mdp8 = ProductMDP(mdp, wdfa8)
solver8 = LPSolver(product_mdp8, path=os.path.join(prefix, "8"), disp=False)
solver8.solve()

value8 = {s[0]: solver8.value[s] for s in product_mdp8.states if s[-1] == "0"}
print(f"The value of the initial state (6, 6) for the F a | F c: {value8[6, 6]}")
print(f"The value of the initial state (3, 0) for the F a | F c: {value8[3, 0]}")
# plot_value_surf(mdp.grid_world_size, value8, path=os.path.join(prefix, "8", "value surf.png"))
plot_heatmap(mdp.grid_world_size, value8, path=os.path.join(prefix, "8", "heatmap.png"))
