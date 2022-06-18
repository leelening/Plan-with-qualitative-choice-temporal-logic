import pytest
from new_mdp import MDP

def test_neighbors():
    mdp = MDP()

    neighbors = mdp.neighbors(np.a)