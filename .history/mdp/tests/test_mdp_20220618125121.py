import pytest
from mdp.new_mdp import MDP
import numpy as np
from itertools import product
from numpy.testing import assert_array_equal

FILE = "/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"


def test_mdp_constructor():
    mdp = MDP(file_path=FILE)


NEIGHBORS_TEST_CASES = (
    ((0, 7), 0, {(0, 7), (1, 7)}),
    ((1, 6), 1, {(2, 6), (1, 5), (1, 7)}),
    ((3, 4), 2, {(3, 3), (4, 4), (2, 4)}),
    ((3, 4), 3, {(3, 3), (3, 5), (2, 4)}),
)


@pytest.mark.parametrize("s,a, expected_neighbors", NEIGHBORS_TEST_CASES)
def test_neighbors(s, a, expected_neighbors):
    mdp = MDP(file_path=FILE)

    neighbors = mdp.neighbors(s, a)

    assert neighbors == expected_neighbors


def test_obstacles_transitions():
    mdp = MDP(file_path=FILE)
    for s, a in product(mdp.obstacles, mdp.actlist):
        assert mdp.transitions[s][a][s] == 1


def test_transitions_sum_to_one():
    mdp = MDP(file_path=FILE)
    for s in mdp.transitions:
        for a in mdp.transitions[s]:
            assert_array_equal(
                np.sum([mdp.transitions[s][a][ns] for ns in mdp.transitions[s][a]]), 1
            )


TRANSITION_TEST_CASES = (
    ((0, 7), 0, (0, 7), 0.9),
    ((0, 7), 0, (1, 7), 0.1),
        ((1, 6), 1, (2, 6), 0.8),
         ((1, 6), 1, (2, 6), 0.8),
    ((3, 4), 2, {(3, 3), (4, 4), (2, 4)}),
    ((3, 4), 3, {(3, 3), (3, 5), (2, 4)}),
)
