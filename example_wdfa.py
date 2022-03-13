__author__ = "Jie Fu and Lening Li"
__email__ = "fujie@ufl.edu and lli4@wpi.edu"
__version__ = "0.0.1"
__maintainer__ = "Jie Fu and Lening Li"
__description__ = (
    "This code provides illustrative examples for creating wdfa and some defined "
    "operations including: orderedOR, prioritized_conj, and prioritized_disj"
)

from WDFA import *
from utils import *


def construct_automaton_example(prefix="figure"):
    check_existence(prefix)

    automaton = dict()
    # Eventually A
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
    dfa1.validate()
    automaton["dfa1"] = dfa1

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
    dfa2.validate()
    automaton["dfa2"] = dfa2

    # not A until B
    dfa3 = DFA(
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
    dfa3.validate()
    automaton["dfa3"] = dfa3

    # try ordered OR between dfa1 and dfa2
    orderedDFA12 = ordered_or(dfa1, dfa2)
    print("Trimming orderedDFA12 ...")
    orderedDFA12.trim()
    orderedDFA12.show_diagram(path="./{}/orderedDFA12.png".format(prefix))
    automaton["orderedDFA12"] = orderedDFA12

    # try ordered OR between dfa3 and dfa1
    orderedDFA31 = ordered_or(dfa3, dfa1)
    print("Trimming orderedDFA31 ...")
    orderedDFA31.trim()
    orderedDFA31.show_diagram(path="./{}/orderedDFA31.png".format(prefix))
    automaton["orderedDFA31"] = orderedDFA31

    # try generalized ordered OR between
    orderedDFA312 = generalized_ordered_or(orderedDFA31, dfa2)
    print("Trimming orderedDFA312 ...")
    orderedDFA312.trim()
    orderedDFA312.show_diagram(path="./{}/orderedDFA312.png".format(prefix))
    automaton["orderedDFA312"] = orderedDFA312

    # create 3 wdfa
    wdfa1 = get_wdfa_from_dfa(dfa1)
    wdfa1.validate()
    automaton["wdfa1"] = wdfa1
    wdfa2 = get_wdfa_from_dfa(dfa2)
    wdfa2.validate()
    automaton["wdfa2"] = wdfa2
    wdfa3 = get_wdfa_from_dfa(dfa3)
    wdfa3.validate()
    automaton["wdfa3"] = wdfa3

    # try the prioritized conjunction between wdfa3 and wdfa2
    conj_wdfa = prioritized_conj(wdfa3, wdfa2)
    print("Trimming conj_wdfa ...")
    conj_wdfa.trim()
    conj_wdfa.show_diagram(path="./{}/conj_wdfa.png".format(prefix))
    automaton["conj_wdfa"] = conj_wdfa

    # try the prioritized disconjunction between wdfa3 and wdfa2
    disj_wdfa = prioritized_disj(wdfa3, wdfa2)
    print("Trimming disj_wdfa ...")
    disj_wdfa.trim()
    disj_wdfa.show_diagram(path="./{}/disj_wdfa.png".format(prefix))
    automaton["disj_wdfa"] = disj_wdfa
    return automaton
