from tkinter import W
import pytest
from automata.fa.dfa import DFA
from itertools import product

from wdfa.helpers import get_wdfa_from_dfa, ordered_or

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

WEIGHT_TEST_CASE = (
    (dfa, "0", "end", "sink", 0),
    (dfa, "0", "a", "1", 0),
    (dfa, "0", "b", "0", 0),
    (dfa, "1", "b", "1", 0),
    (dfa, "1", "end", "sink", 1),
)


@pytest.mark.parametrize("dfa, q, a, nq, w", WEIGHT_TEST_CASE)
def test_weights(dfa, q, a, nq, w):
    wdfa = get_wdfa_from_dfa(dfa)
    assert wdfa.weight[q, a, nq] == w


def test_completeness():
    wdfa = get_wdfa_from_dfa(dfa)
    for q, a in product(wdfa.states, wdfa.input_symbols):
        assert wdfa.transitions[q][a] in wdfa.states


ORDERED_OR_TEST_CASE = (
    (("0", "0"), "E", ("0", "0"), 0),
    (
        ("0", "0"),
        "a",
        ("1", "0"),
        0,
    ),
    (("1", "1"), "end", "sink", 1),
)


@pytest.mark.parametrize("q, a, nq, w", ORDERED_OR_TEST_CASE)
def test_ordered_or(
    get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa, q, a, nq, w
):
    wdfa = ordered_or(get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa)
    print(get_wdfa_from_eventually_a_dfa)
    assert wdfa.weight[q, a, nq] == w
