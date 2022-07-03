from wdfa.helpers import get_wdfa_from_dfa, check_dir, prioritized_conj
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_10, DFA_11
from solver.lp_solver import LPSolver
from simulation.simulator import Simulator
from utils import save_trajectories, plot_value_surf

prefix = "example_6"

check_dir(prefix)


wdfa10 = get_wdfa_from_dfa(
    DFA_10, path=prefix, name="(!b & !c) U (a & (!c U (b & Fc)))"
)
wdfa11 = get_wdfa_from_dfa(
    DFA_11, path=prefix, name="(F a -> F (b & F c) )& (F a & F b & F c)"
)


prod_wdfa = prioritized_conj(
    wdfa10,
    wdfa11,
    path=prefix,
    name=prefix,
)

print(prod_wdfa)


mdp = MDP(
    file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"
)

product_mdp = ProductMDP(mdp, prod_wdfa)


solver = LPSolver(product_mdp, path=prefix, disp=False)

solver.solve()

value = {s[0]: solver.value[s] for s in product_mdp.states if s[-1] == ("0", "0")}


plot_value_surf(
    mdp.grid_world_size,
    value,
    title="(!b & !c) U (a & (!c U (b & Fc))) OR (F a -> F (b & F c) )& (F a & F b & F c)",
)

simulator = Simulator(mdp=product_mdp, policy=solver.policy)

sampled_trajectories = simulator.sample_trajectories(10)

save_trajectories(sampled_trajectories=sampled_trajectories, prefix=prefix)
