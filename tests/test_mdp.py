import pytest
import numpy as np
from itertools import product
from numpy.testing import assert_array_equal

from mdp.mdp import MDP


FILE = "/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"


def test_mdp_constructor():
    mdp = MDP(file_path=FILE)


NEIGHBORS_TEST_CASES = (
    ((0, 7), 0, {(0, 7), (1, 7)}),
    ((1, 6), 1, {(2, 6), (1, 5), (1, 7)}),
    ((3, 4), 2, {(3, 3), (4, 4), (2, 4)}),
    ((3, 4), 3, {(2, 4), (3, 3), (3, 5)}),
)


@pytest.mark.parametrize("s, a, expected_neighbors", NEIGHBORS_TEST_CASES)
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


DETERMINISTIC_TRANSITION_TEST_CASES = (((0, 7), 0, (0, 7)), ((0, 7), 1, (1, 7)))


@pytest.mark.parametrize("s, a, ns", DETERMINISTIC_TRANSITION_TEST_CASES)
def test_deterministic_transitions(s, a, ns):
    mdp = MDP(file_path=FILE)
    assert ns == mdp.deterministic_transition(s, a)


TRANSITION_TEST_CASES = (
    ((0, 7), 0, (0, 7), 0.9),
    ((0, 7), 0, (1, 7), 0.1),
    ((1, 6), 1, (2, 6), 0.8),
    ((1, 6), 1, (1, 5), 0.1),
    ((1, 6), 1, (1, 7), 0.1),
    ((3, 4), 2, (3, 3), 0.8),
    ((3, 4), 2, (4, 4), 0.1),
    ((3, 4), 2, (2, 4), 0.1),
    ((3, 4), 3, (2, 4), 0.8),
    ((3, 4), 3, (3, 3), 0.1),
    ((3, 4), 3, (3, 5), 0.1),
)


@pytest.mark.parametrize("s, a, ns, p", TRANSITION_TEST_CASES)
def test_transition(s, a, ns, p):
    mdp = MDP(file_path=FILE)
    assert_array_equal(mdp.transitions[s][a][ns], p)


def test_print():
    mdp = MDP(file_path=FILE)
    print(mdp)


def test_labels():
    mdp = MDP(file_path=FILE)
    for s in mdp.states:
        assert mdp.L[s] in mdp.AP
