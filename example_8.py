from wdfa.helpers import get_wdfa_from_dfa, ordered_or, check_dir
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_2, DFA_8, DFA_12
from solver.lp_solver import LPSolver
from solver.lp_evaluator import LPEvaluator
from utils import plot_value_surf, plot_heatmap
import os
from utils import read_policy, projected_policy

prefix = "example_8"

check_dir(prefix)

wdfa2 = get_wdfa_from_dfa(DFA_2, path=prefix, name="F b")
wdfa8 = get_wdfa_from_dfa(DFA_8, path=prefix, name="F a | F c")
wdfa12 = get_wdfa_from_dfa(DFA_12, path=prefix, name="F b | (F a | F c)")
wdfa = ordered_or(wdfa2, wdfa8, path=prefix, name="F b OR (F a | F c)")

mdp = MDP(
    file_path="environment/8 x 8/1.yaml"
)

product_mdp = ProductMDP(mdp, wdfa)
product_mdp2 = ProductMDP(mdp, wdfa2)
product_mdp8 = ProductMDP(mdp, wdfa8)
product_mdp12 = ProductMDP(mdp, wdfa12)

solver = LPSolver(product_mdp12, path=prefix, disp=False)
solver.solve()

policy = read_policy(os.path.join("example_8", "policy.tsv"))

evaluator = LPEvaluator(product_mdp, policy_path=os.path.join("example_8", "policy.tsv"), disp=False)

evaluator2 = LPEvaluator(product_mdp2, policy_path=os.path.join("example_8", "policy.tsv"), disp=False)
evaluator2.set_policy(projected_policy(policy, col=0))

evaluator8 = LPEvaluator(product_mdp8, policy_path=os.path.join("example_8", "policy.tsv"), disp=False)
evaluator8.set_policy(projected_policy(policy, col=1))

evaluator.evaluate()
value = {s[0]: evaluator.value[s] for s in product_mdp.states if s[-1] == ("0", "0")}

evaluator2.evaluate()
value2 = {s[0]: evaluator2.value[s] for s in product_mdp2.states if s[-1] == "0"}

evaluator8.evaluate()
value8 = {s[0]: evaluator8.value[s] for s in product_mdp8.states if s[-1] == "0"}

plot_value_surf(mdp.grid_world_size, value, path=os.path.join(prefix, "0", "value surf.png"))
plot_heatmap(mdp.grid_world_size, value, path=os.path.join(prefix, "0", "heatmap.png"))

plot_value_surf(mdp.grid_world_size, value2, path=os.path.join(prefix, "2", "value surf.png"))
plot_heatmap(mdp.grid_world_size, value2, path=os.path.join(prefix, "2", "heatmap.png"))

plot_value_surf(mdp.grid_world_size, value8, path=os.path.join(prefix, "8", "value surf.png"))
plot_heatmap(mdp.grid_world_size, value8, path=os.path.join(prefix, "8", "heatmap.png"))
