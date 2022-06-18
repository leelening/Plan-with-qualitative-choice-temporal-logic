from automata.fa.dfa import DFA

from wdfa.helpers import get_wdfa_from_dfa, sync

dfa1 = DFA(
    states={"0", "1"},
    input_symbols={"a", "b", "E"},
    transitions={
        "0": {"a": "1", "b": "0", "E": "0"},
        "1": {"a": "1", "b": "1", "E": "1"},
    },
    initial_state="0",
    final_states={"1"},
)

# eventually B
dfa2 = DFA(
    states={"0", "1"},
    input_symbols={"a", "b", "E"},
    transitions={
        "0": {"a": "0", "b": "1", "E": "0"},
        "1": {"a": "1", "b": "1", "E": "1"},
    },
    initial_state="0",
    final_states={"1"},
)


def test_get_wdfa_from_dfa():
    wdfa1 = get_wdfa_from_dfa(dfa1)
    wdfa2 = get_wdfa_from_dfa(dfa2)


def test_set_options():
    wdfa1 = get_wdfa_from_dfa(dfa1)
    wdfa1.set_option(10)
    wdfa1.validate()
    assert wdfa1.opt == 10


def test_sync():
    wdfa1 = get_wdfa_from_dfa(dfa1)
    wdfa2 = get_wdfa_from_dfa(dfa2)

    sync_dfa = sync(wdfa1, wdfa2)
