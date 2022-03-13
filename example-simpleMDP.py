from torch._jit_internal import ignore

from mdp import MDP
from product_mdp import ProductMDP
import os
import pandas as pd

print("Initializing the MPD ...")
mdp = MDP(file_path="ex.yaml")
print("Validating the MDP ...")
mdp.validate()
print("Finish validation of MDP! Printing the detailed information ...")
print(mdp)
print("Finish printing the MDP ...")
print("Saving the MDP info into ./MDP.csv")
mdp.save()

print("Initializing the WDFA ...")
exec(open("./example-wdfa.py").read())
print("Constructing the product MDP ...")
# the objective is to reach a state labeled 'b'.
automaton = "orderedDFA12"
product_mdp = ProductMDP(mdp, orderedDFA12)
print("Validating the product MDP ...")
# explicitly validate the mdp
product_mdp.validate()
print("Finish validation of product MDP! Printing the detailed information ...")
print(product_mdp)
print("Saving the Product MDP info into ./ProductMDP.csv")
product_mdp.save()

from lp_mdp import LP

print("Start computing the product MDP ...")
df = LP(product_mdp)
print("End of the computation of the product MDP...")
print("Saving results of product MDP ...")
df.to_csv("./results.csv")

print("Start simulating the product MDP ...")
state = product_mdp.init


counter = 0
trajectory = []
trajectory.append((state,))
while counter <= 100 and state != "v_sink":
    index = df["state"] == state
    action = df.loc[index]["policy"].values[0]
    next_state = product_mdp.step(state, action)
    trajectory.append((action, product_mdp.reward[state, action], next_state))
    state = next_state
    counter += 1

print("Finish simulating the product MDP ...")
print("Printing trajectory ...")
print("Trajectory: {}".format([x[-1][0] for x in trajectory]))
print("Saving trajectory ...")
if os.path.exists("trajectory.csv"):
    df1 = pd.read_csv("trajectory.csv")
else:
    df1 = pd.DataFrame({"Description": [], "Trajectory": []})
df1 = df1.append(
    {
        "Description": "mdp_{}_automaton_{}".format(mdp.name, str(automaton)),
        "Trajectory": trajectory,
        "States": [x[-1][0] for x in trajectory],
    },
    ignore_index=True,
)
df1.to_csv("trajectory.csv", index=False)
print("End")
