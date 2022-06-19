from wdfa.helpers import get_wdfa_from_dfa, ordered_or
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_6, DFA_7
from solver.lp import LPSolver

wdfa6 = get_wdfa_from_dfa(DFA_6)
wdfa7 = get_wdfa_from_dfa(DFA_7)


wdfa = ordered_or(wdfa6, wdfa7)


mdp = MDP(
    file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"
)

product_mdp = ProductMDP(mdp, wdfa)


solver = LPSolver(product_mdp, path="example_1", print=True)

solver.solve()
