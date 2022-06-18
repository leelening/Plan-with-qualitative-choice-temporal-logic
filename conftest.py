import pytest
from automata.fa.dfa import DFA

from mdp.mdp import MDP
from wdfa.helpers import get_wdfa_from_dfa


@pytest.fixture
def construct_eventually_a_dfa():
    # eventually A
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
    # eventually B
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
