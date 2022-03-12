from MDP import MDP as M
from ProductMDP import *

mdp = M(file_path="ex.yaml")
mdp.validate()
print(mdp)

# exec(open("./example-wdfa.py").read())
# # the objective is to reach a state labeled 'b'.
# productmdp, reward = product_mdp(mdp, orderedDFA12)
# from Policy import *
#
# Vstate1, policyT = value_iter(productmdp, reward)
# print("end")
