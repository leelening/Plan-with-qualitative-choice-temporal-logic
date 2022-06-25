import pytest
import numpy as np
from itertools import product
from numpy.testing import assert_array_equal

from mdp.mdp import MDP


NEIGHBORS_TEST_CASES = (
    ((0, 7), 0, {(0, 7), (1, 7)}),
    ((1, 6), 1, {(2, 6), (1, 5), (1, 7)}),
    ((3, 4), 2, {(3, 3), (4, 4), (2, 4)}),
    ((3, 4), 3, {(2, 4), (3, 3), (3, 5)}),
)

DETERMINISTIC_TRANSITION_TEST_CASES = (((0, 7), 0, (0, 7)), ((0, 7), 1, (1, 7)))

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
    ("sT", 0, "sT", 1),
    ((3, 4), "aT", "sT", 1),
    ((6, 2), "aT", "sT", 1),
)


@pytest.mark.parametrize("s, a, expected_neighbors", NEIGHBORS_TEST_CASES)
def test_neighbors(construct_mdp, s, a, expected_neighbors):
    mdp = construct_mdp
    neighbors = mdp.neighbors(s, a)
    assert neighbors == expected_neighbors


def test_obstacles_transitions(construct_mdp):
    mdp = construct_mdp
    for s, a in product(mdp.obstacles, mdp.actlist):
        if a != "aT":
            n_d_s = mdp.deterministic_transition(s, a)
            if n_d_s == s:
                assert mdp.transitions[s][a][s] == 1
            else:
                assert mdp.transitions[s][a][s] == mdp.stuck_prob
                assert mdp.transitions[s][a][n_d_s] == 1 - mdp.stuck_prob
        else:
            assert mdp.transitions[s][a]["sT"] == 1


def test_transitions_sum_to_one(construct_mdp):
    mdp = construct_mdp
    for s in mdp.transitions:
        for a in mdp.transitions[s]:
            assert_array_equal(
                np.sum([mdp.transitions[s][a][ns] for ns in mdp.transitions[s][a]]), 1
            )


@pytest.mark.parametrize("s, a, ns", DETERMINISTIC_TRANSITION_TEST_CASES)
def test_deterministic_transitions(construct_mdp, s, a, ns):
    mdp = construct_mdp
    assert ns == mdp.deterministic_transition(s, a)


@pytest.mark.parametrize("s, a, ns, p", TRANSITION_TEST_CASES)
def test_transition(construct_mdp, s, a, ns, p):
    mdp = construct_mdp
    assert_array_equal(mdp.transitions[s][a][ns], p)


def test_print(construct_mdp):
    mdp = construct_mdp
    print(mdp)


def test_labels(construct_mdp):
    mdp = construct_mdp
    for s in mdp.states:
        assert mdp.L[s] in mdp.AP


TEST_CASE_DETERMINISTIC_TRANSITION = (
    ((4, 3), 1, (4, 3)),
    ((4, 4), 0, (4, 5)),
    ((6, 5), 1, (7, 5)),
    ((6, 5), 2, (6, 4)),
    ((6, 5), 3, (5, 5)),
)


@pytest.mark.parametrize("s, a, n_d_s", TEST_CASE_DETERMINISTIC_TRANSITION)
def test_deterministic_transition(construct_mdp, s, a, n_d_s):
    mdp = construct_mdp
    assert mdp.deterministic_transition(s, a) == n_d_s


def test_stochastic_transitions(construct_mdp):
    mdp = construct_mdp
    for s, a in product(mdp.states, mdp.actlist):
        assert mdp.stochastic_transition(s, a) in list(mdp.transitions[s][a].keys())
