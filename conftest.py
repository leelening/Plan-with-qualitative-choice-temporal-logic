import pytest
from automata.fa.dfa import DFA
from collections import defaultdict

from mdp.mdp import MDP
from wdfa.helpers import get_wdfa_from_dfa
from product_mdp.product_mdp import ProductMDP


@pytest.fixture
def construct_eventually_a_dfa():
    dfa = DFA(
        states={"0", "1"},
        input_symbols={"a", "b", "E"},
        transitions={
            "0": {"a": "1", "b": "0", "E": "0"},
            "1": {"a": "1", "b": "1", "E": "1"},
        },
        initial_state="0",
        final_states={"1"},
    )
    return dfa


@pytest.fixture
def construct_eventually_b_dfa():
    dfa = DFA(
        states={"0", "1"},
        input_symbols={"a", "b", "E"},
        transitions={
            "0": {"a": "0", "b": "1", "E": "0"},
            "1": {"a": "1", "b": "1", "E": "1"},
        },
        initial_state="0",
        final_states={"1"},
    )
    return dfa


@pytest.fixture
def construct_not_a_until_b_dfa():
    dfa = DFA(
        states={"0", "1", "2"},
        input_symbols={"a", "b", "E"},
        transitions={
            "0": {"a": "2", "b": "1", "E": "0"},
            "1": {"a": "1", "b": "1", "E": "1"},
            "2": {"a": "2", "b": "2", "E": "2"},
        },
        initial_state="0",
        final_states={"1"},
    )
    return dfa


@pytest.fixture
def construct_mdp():
    return MDP(
        file_path="/home/lening/Desktop/qualitative_choice_logic/environment/8 x 8/1.yaml"
    )


@pytest.fixture
def get_wdfa_from_eventually_a_dfa(construct_eventually_a_dfa):
    wdfa = get_wdfa_from_dfa(construct_eventually_a_dfa)
    return wdfa


@pytest.fixture
def get_wdfa_from_eventually_b_dfa(construct_eventually_b_dfa):
    wdfa = get_wdfa_from_dfa(construct_eventually_b_dfa)
    return wdfa


@pytest.fixture
def get_wdfa_from_not_a_until_b_dfa(construct_not_a_until_b_dfa):
    wdfa = get_wdfa_from_dfa(construct_not_a_until_b_dfa)
    return wdfa


@pytest.fixture
def construct_product_mdp(construct_mdp, get_wdfa_from_eventually_a_dfa):
    return ProductMDP(construct_mdp, get_wdfa_from_eventually_a_dfa)


@pytest.fixture
def construct_mdp_with_reward_1(construct_mdp):
    mdp = construct_mdp
    mdp.reward = defaultdict(float)
    mdp.reward[(2, 0), 3] = 1
    mdp.reward[(1, 1), 2] = 1
    mdp.reward[(0, 0), 1] = 1
    mdp.gamma = 0.9

    for a in mdp.actlist:
        for ns in mdp.transitions[1, 0][a]:
            mdp.transitions[1, 0][a][ns] = 0
    return mdp


@pytest.fixture
def construct_mdp_with_reward_2(construct_mdp):
    mdp = construct_mdp
    mdp.reward = defaultdict(float)
    mdp.reward[(2, 6), 3] = 1
    mdp.reward[(1, 5), 0] = 1
    mdp.reward[(0, 6), 1] = 1
    mdp.reward[(1, 9), 2] = 1
    mdp.gamma = 0.9

    for a in mdp.actlist:
        for ns in mdp.transitions[1, 6][a]:
            mdp.transitions[1, 6][a][ns] = 0
    return mdp
