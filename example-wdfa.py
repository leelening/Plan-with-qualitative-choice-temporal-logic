__author__ = "Jie Fu and Lening Li"
__email__ = "fujie@ufl.edu and lli4@wpi.edu"
__version__ = "0.0.1"
__maintainer__ = "Jie Fu and Lening Li"
__description__ = (
    "This code provides illustrative examples for creating wdfa and some defined "
    "operations including: orderedOR, prioritized_conj, and prioritized_disj"
)

from WDFA import *

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

# try ordered OR between dfa1 and dfa2
orderedDFA12 = orderedOR(dfa1, dfa2)
orderedDFA12.show_diagram(path="./orderedDFA12.png")

# try ordered OR between dfa3 and dfa2
orderedDFA = orderedOR(dfa3, dfa2)
orderedDFA.show_diagram(path="./orderedDFA.png")

# try generalized ordered OR between
orderedDFA2 = generalized_orderedOR(orderedDFA, dfa1)
orderedDFA2.show_diagram(path="./orderedDFA2.png")

# create 3 wdfa
wdfa1 = get_wdfa_from_dfa(dfa1)
wdfa1.validate()
wdfa2 = get_wdfa_from_dfa(dfa2)
wdfa2.validate()
wdfa3 = get_wdfa_from_dfa(dfa3)
wdfa3.validate()

# try the prioritized conjunction between wdfa3 and wdfa2
conj_wdfa = prioritized_conj(wdfa3, wdfa2)
conj_wdfa.trim()
conj_wdfa.show_diagram(path="./conj_wdfa.png")

# try the prioritized disconjunction between wdfa3 and wdfa2
disj_wdfa = prioritized_disj(wdfa3, wdfa2)
disj_wdfa.show_diagram(path="./disj_wdfa.png")
