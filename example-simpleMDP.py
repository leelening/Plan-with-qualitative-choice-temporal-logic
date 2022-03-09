from MDP import *
from ProductMDP import *

mdp = read_from_file_MDP("ex.txt")
mdp.init = 0
for s in mdp.states:
    mdp.labeling(s, "E")  # 'E' is for neither a or b.
mdp.labeling(3, "a")
mdp.labeling(6, "b")
Labels = ["a", "b", "E"]

exec(open("./example-wdfa.py").read())
# the objective is to reach a state labeled 'b'.
productmdp, reward = product_mdp(mdp, orderedDFA12)
from Policy import *

Vstate1, policyT = value_iter(productmdp, reward)
print("end")
