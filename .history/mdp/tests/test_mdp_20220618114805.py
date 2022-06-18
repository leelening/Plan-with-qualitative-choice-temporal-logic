import pytest
from mdp.new_mdp import MDP
import numpy as np

def test_neighbors():
    mdp = MDP(file_path="environment/8 x 8/1.yaml")

    neighbors = mdp.neighbors(np.array([0, 7]), 0)

    assert neighbors == set([np.array([0, 7]),np.array([1, 7])])
