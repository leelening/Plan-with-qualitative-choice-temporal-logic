import pytest
from mdp.new_mdp import MDP
import numpy as np

def test_neighbors():
    mdp = MDP(file_path="../../../en)

    neighbors = mdp.neighbors(np.array([0, 7]), 0)

    assert neighbors == set([np.array([0, 7]),np.array([1, 7])])
