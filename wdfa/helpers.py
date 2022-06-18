from automata.fa.dfa import DFA
from wdfa.wdfa import WDFA
from itertools import product


def get_wdfa_from_dfa(dfa: DFA) -> WDFA:
    """
    Return a wdfa from a given dfa

    :param: dfa: given a dfa
    :return the converted wdfa
    """

    wdfa = WDFA(
        dfa.states,
        dfa.input_symbols,
        dfa.transitions,
        dfa.initial_state,
        dfa.final_states,
    )
    wdfa.states.add("sink")
    wdfa.input_symbols.add("end")
    wdfa.transitions["sink"] = {a: "sink" for a in wdfa.input_symbols}
    for a in wdfa.input_symbols:
        wdfa.assign_weight("sink", a, "sink", 0)

    for q in wdfa.states:
        if q != "sink":
            wdfa.transitions[q]["end"] = "sink"
        wdfa.assign_weight(q, "end", "sink", 1)

    wdfa.set_option(1)
    wdfa.validate()
    return wdfa
