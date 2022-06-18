import pytest
from src.new_mdp import MDP
import numpy as np

def test_neighbors():
    mdp = MDP()

    neighbors = mdp.neighbors(np.array([0, 7]), 0)

    assert neighbors == set([np.array([0, 7]),np.array([1, 7])])
