from wdfa.helpers import get_wdfa_from_dfa
from automata.fa.dfa import DFA

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


def test_get_wdfa_from_dfa(dfa):
    wdfa = get_wdfa_from_dfa(dfa)
    wdfa.validate()
