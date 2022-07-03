from wdfa.helpers import get_wdfa_from_dfa, ordered_or, check_dir, prioritized_conj
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_6, DFA_7, DFA_2, DFA_8
from solver.lp_solver import LPSolver
from simulation.simulator import Simulator
from utils import save_trajectories, plot_value_surf

prefix = "example_4"

check_dir(prefix)


wdfa6 = get_wdfa_from_dfa(DFA_6, path=prefix, name="F(a & F(b & F c))")
wdfa7 = get_wdfa_from_dfa(DFA_7, path=prefix, name="F (a & F c) | F (b & F c)")

wdfa2 = get_wdfa_from_dfa(DFA_2, path=prefix, name="F b")
wdfa8 = get_wdfa_from_dfa(DFA_8, path=prefix, name="F a | F c")


prod_wdfa = prioritized_conj(
    ordered_or(wdfa6, wdfa7), ordered_or(wdfa2, wdfa8), path=prefix, name="example_4"
)


mdp = MDP(
    file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/2.yaml"
)

product_mdp = ProductMDP(mdp, prod_wdfa)


solver = LPSolver(product_mdp, path=prefix, disp=False)

solver.solve()

value = {
    s[0]: solver.value[s]
    for s in product_mdp.states
    if s[-1] == (("0", "0"), ("0", "0"))
}

plot_value_surf(mdp.grid_world_size, value)

simulator = Simulator(mdp=product_mdp, policy=solver.policy)

sampled_trajectories = simulator.sample_trajectories(10)

save_trajectories(sampled_trajectories=sampled_trajectories, prefix=prefix)