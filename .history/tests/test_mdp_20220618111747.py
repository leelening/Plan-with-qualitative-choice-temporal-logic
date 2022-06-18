import pytest
from new_mdp import MDP
import numpy as np

def test_neighbors():
    mdp = MDP()

    neighbors = mdp.neighbors(np.array([0, 7]), 0)

    neighbors = mdp.neighbors
