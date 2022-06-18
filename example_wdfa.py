__author__ = "Jie Fu and Lening Li"
__email__ = "fujie@ufl.edu and lli4@wpi.edu"
__version__ = "0.0.1"
__maintainer__ = "Jie Fu and Lening Li"
__description__ = (
    "This code provides illustrative examples for creating wdfa and some defined "
    "operations including: orderedOR, prioritized_conj, and prioritized_disj"
)

from wdfa.wdfa.wdfa import *
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

    # !p3 U ((p1 & (!(p2 | p3) U p5)) | (p2 & (!(p1 | p3) U p4)))
    dfa4 = DFA(
        states={"0", "1", "2", "3", "4"},
        input_symbols={"a", "b", "E", "c", "d", "o"},
        transitions={
            "2": {"a": "3", "b": "2", "E": "2", "c": "1", "d": "2", "o": "4"},
            "0": {"a": "0", "b": "0", "E": "0", "c": "0", "d": "0", "o": "0"},
            "1": {"a": "3", "b": "1", "E": "1", "c": "1", "d": "0", "o": "4"},
            "3": {"a": "3", "b": "0", "E": "3", "c": "1", "d": "3", "o": "4"},
            "4": {"a": "4", "b": "4", "E": "4", "c": "4", "d": "4", "o": "4"},
        },
        initial_state="2",
        final_states={"0"},
    )
    dfa4.validate()
    automaton["dfa4"] = dfa4

    # !p3 U (p2 & XFp4)  &  !p3 U (p1 & XFp5)
    dfa5 = DFA(
        states={"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"},
        input_symbols={"a", "b", "E", "c", "d", "o"},
        transitions={
            "0": {"a": "0", "b": "0", "E": "0", "c": "0", "d": "0", "o": "0"},
            "1": {"a": "5", "b": "1", "E": "1", "c": "7", "d": "1", "o": "9"},
            "2": {"a": "2", "b": "2", "E": "2", "c": "2", "d": "0", "o": "9"},
            "3": {"a": "3", "b": "2", "E": "3", "c": "3", "d": "4", "o": "9"},
            "4": {"a": "4", "b": "0", "E": "4", "c": "4", "d": "4", "o": "9"},
            "5": {"a": "5", "b": "6", "E": "5", "c": "3", "d": "5", "o": "9"},
            "6": {"a": "6", "b": "6", "E": "6", "c": "2", "d": "6", "o": "9"},
            "7": {"a": "3", "b": "7", "E": "7", "c": "7", "d": "8", "o": "9"},
            "8": {"a": "4", "b": "8", "E": "8", "c": "8", "d": "8", "o": "9"},
            "9": {"a": "9", "b": "9", "E": "9", "c": "9", "d": "9", "o": "9"},
        },
        initial_state="1",
        final_states={"0"},
    )
    dfa5.validate()
    automaton["dfa5"] = dfa5

    print("Saving constructed dfa1, dfa2, dfa3 ...")
    dfa1.show_diagram(path="./{}/dfa1.png".format(prefix))
    dfa2.show_diagram(path="./{}/dfa2.png".format(prefix))
    dfa3.show_diagram(path="./{}/dfa3.png".format(prefix))
    dfa4.show_diagram(path="./{}/dfa4.png".format(prefix))
    dfa5.show_diagram(path="./{}/dfa5.png".format(prefix))

    # try ordered OR between dfa1 and dfa2
    orderedDFA12 = ordered_or(dfa1, dfa2)
    print("Trimming orderedDFA12 ...")
    orderedDFA12.trim()
    orderedDFA12.show_diagram(path="./{}/orderedDFA12.png".format(prefix))
    automaton["orderedDFA12"] = orderedDFA12

    # try ordered OR between dfa4 and dfa5
    orderedDFA45 = ordered_or(dfa4, dfa5)
    print("Trimming orderedDFA45 ...")
    orderedDFA45.trim()
    orderedDFA45.show_diagram(path="./{}/orderedDFA45.png".format(prefix))
    automaton["orderedDFA45"] = orderedDFA45

    # try ordered OR between dfa3 and dfa1
    orderedDFA31 = ordered_or(dfa3, dfa1)
    print("Trimming orderedDFA31 ...")
    orderedDFA31.trim()
    orderedDFA31.show_diagram(path="./{}/orderedDFA31.png".format(prefix))
    automaton["orderedDFA31"] = orderedDFA31

    # try ordered OR between dfa3 and dfa2
    orderedDFA32 = ordered_or(dfa3, dfa2)
    print("Trimming orderedDFA32 ...")
    orderedDFA32.trim()
    orderedDFA32.show_diagram(path="./{}/orderedDFA32.png".format(prefix))
    automaton["orderedDFA32"] = orderedDFA32

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

    # try the prioritized conjunction between wdfa3 and wdfa1
    conj_wdfa31 = prioritized_conj(wdfa3, wdfa1)
    print("Trimming conj_wdfa31 ...")
    conj_wdfa31.trim()
    conj_wdfa31.show_diagram(path="./{}/conj_wdfa31.png".format(prefix))
    automaton["conj_wdfa31"] = conj_wdfa31

    # try the prioritized disconjunction between wdfa3 and wdfa1
    disj_wdfa31 = prioritized_disj(wdfa3, wdfa1)
    print("Trimming disj_wdfa31 ...")
    disj_wdfa31.trim()
    disj_wdfa31.show_diagram(path="./{}/disj_wdfa31.png".format(prefix))
    automaton["disj_wdfa31"] = disj_wdfa31

    # try the prioritized conjunction between orderedDFA31 and orderedDFA12
    conj_wdfa3112 = prioritized_conj(orderedDFA31, orderedDFA12)
    print("Trimming conj_wdfa3112 ...")
    conj_wdfa3112.trim()
    conj_wdfa3112.show_diagram(path="./{}/conj_wdfa3112.png".format(prefix))
    automaton["conj_wdfa3112"] = conj_wdfa3112

    # try the prioritized disconjunction between orderedDFA31 and orderedDFA12
    disj_wdfa3112 = prioritized_disj(orderedDFA31, orderedDFA12)
    print("Trimming disj_wdfa3112 ...")
    disj_wdfa3112.trim()
    disj_wdfa3112.show_diagram(path="./{}/disj_wdfa3112.png".format(prefix))
    automaton["disj_wdfa3112"] = disj_wdfa3112

    # try the prioritized conjunction between orderedDFA45 and orderedDFA12
    conj_wdfa4512 = prioritized_conj(orderedDFA45, orderedDFA12)
    print("Trimming conj_wdfa4512 ...")
    conj_wdfa4512.trim()
    conj_wdfa4512.show_diagram(path="./{}/conj_wdfa4512.png".format(prefix))
    automaton["conj_wdfa4512"] = conj_wdfa4512
    return automaton
