from mdp import MDP
from product_mdp import ProductMDP
import pandas as pd
from example_wdfa import construct_automaton_example
from utils import *

prefix = "./environment"
#####
file = "deterministic_gridworld_feasible_a"
# file = "deterministic_gridworld_infeasible_a"
# file = "stochastic_gridworld_feasible_a"
# file = "stochastic_gridworld_infeasible_a"

# spec = "orderedDFA12"
# spec = "orderedDFA31"
# spec = "orderedDFA312"
# spec = "conj_wdfa31"
# spec = "disj_wdfa31"
# spec = "conj_wdfa3112"
spec = "disj_wdfa3112"

file_path = prefix + "/{}.yaml".format(file)
path = file + "_" + spec
check_existence(path)
#####
print("Initializing the MPD ...")
mdp = MDP(file_path=file_path)
print("Validating the MDP ...")
mdp.validate()
print("Finish validation of MDP! Printing the detailed information ...")
print(mdp)
print("Finish printing the MDP ...")
print("Saving the MDP info into ./MDP.csv")
mdp.save(path)

print("Initializing the WDFA ...")
automaton = construct_automaton_example()
print("Constructing the product MDP ...")
# the objective is to reach a state labeled 'b'.
product_mdp = ProductMDP(mdp, automaton[spec])
print("Validating the product MDP ...")
# explicitly validate the mdp
product_mdp.validate()
print("Finish validation of product MDP! Printing the detailed information ...")
print(product_mdp)
print("Saving the Product MDP info into ./ProductMDP.csv")
product_mdp.save(path)

from lp_mdp import LP

print("Start computing the product MDP ...")
df = LP(product_mdp)
print("End of the computation of the product MDP...")
print("Saving results of product MDP ...")
df.to_csv("./{}/results.csv".format(path))

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
    print(
        "grid state: {}, action: {}, reward: {}, next_state: {}.".format(
            state, action, product_mdp.reward[state, action], next_state
        )
    )
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
        "Description": "mdp_{}_automaton_{}".format(file, spec),
        "Trajectory": trajectory,
        "States": [x[-1][0] for x in trajectory],
    },
    ignore_index=True,
)
df1.to_csv("trajectory.csv", index=False)
print("End")
