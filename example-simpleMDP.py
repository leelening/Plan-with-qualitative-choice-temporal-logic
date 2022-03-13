from mdp import MDP
from product_mdp import ProductMDP

print("Initialize the MPD ...")
mdp = MDP(file_path="ex.yaml")
print("Validate the MDP ...")
mdp.validate()
print("Finish validation of MDP! Printing the detailed information ...")
print(mdp)
print("Finish printing the MDP ...")

print("Initialize the WDFA ...")
exec(open("./example-wdfa.py").read())
print("Construct the product MDP ...")
# the objective is to reach a state labeled 'b'.
product_mdp = ProductMDP(mdp, orderedDFA12)
print("Validate the product MDP ...")
# explicitly validate the mdp
product_mdp.validate()
print("Finish validation of product MDP! Printing the detailed information ...")
print(product_mdp)

from lp_mdp import LP

print("Start computing the product MDP ...")
df = LP(product_mdp)
print("End of the computation of the product MDP...")
print("Save results of product MDP ...")
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
print("Trajectory: {}".format([x[-1][0] for x in trajectory]))
