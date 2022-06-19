from wdfa.helpers import get_wdfa_from_dfa, ordered_or, check_dir
from product_mdp.product_mdp import ProductMDP
from mdp.mdp import MDP
from dfa.examples import DFA_2, DFA_8
from solver.lp import LPSolver

prefix = "example_2"

check_dir(prefix)


wdfa2 = get_wdfa_from_dfa(DFA_2, path="{}/F b.png".format(prefix))
wdfa8 = get_wdfa_from_dfa(DFA_8, path="{}/F a | F c.png".format(prefix))


wdfa = ordered_or(wdfa2, wdfa8, path="{}/{}.png".format(prefix, prefix))


mdp = MDP(
    file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"
)

product_mdp = ProductMDP(mdp, wdfa)


solver = LPSolver(product_mdp, path=prefix, print=False)

solver.solve()
