import pytest
from mdp.new_mdp import MDP
import numpy as np

FILE = "/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"


def test_mdp_constructor():
    mdp = MDP(file_path=FILE)


NEIGHBORS_TEST_CASE_ = (
    ((1, 7), 0, ((0, 7), (1, 7))),
    ((1, 6), 1, (2, 6), (1, 5), (1, 7)),
    ((3, 4), 2, (3, 3), (4, 4), (2, 4)),
)

@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
)
def test_neighbors():
    mdp = MDP(file_path=FILE)

    neighbors = mdp.neighbors(np.array([0, 7]), 0)

    assert neighbors == set([(0, 7), (1, 7)])
