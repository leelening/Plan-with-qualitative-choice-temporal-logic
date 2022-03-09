# illustrative examples

from automata.fa.dfa import DFA
from WDFA import *

# Eventually A
dfa = DFA(
    states={'0', '1'},
    input_symbols={'a', 'b', 'E'},
    transitions={
        '0': {'a': '1', 'b': '0', 'E': '0'},
        '1': {'a': '1', 'b': '1', 'E': '1'}
    },
    initial_state='0',
    final_states={'1'}
)


# eventually B
dfa2 = DFA(
    states={'0', '1'},
    input_symbols={'a', 'b','E'},
    transitions={
        '0': {'a': '0', 'b': '1', 'E': '0'},
        '1': {'a': '1', 'b': '1',  'E': '1'}
    },
    initial_state='0',
    final_states={'1'}
)

# not A until B
dfa3 = DFA(
    states={'0', '1', '2'},
    input_symbols={'a', 'b', 'E'},
    transitions={
        '0': {'a': '2', 'b': '1', 'E': '0'},
        '1': {'a': '1', 'b': '1', 'E': '1'},
        '2': {'a': '2', 'b': '2', 'E': '2'},
    },
    initial_state='0',
    final_states={'1'}
)
wdfa1 =  get_wdfa_from_dfa(dfa)
wdfa2  = get_wdfa_from_dfa(dfa2)
wdfa3  = get_wdfa_from_dfa(dfa3)
orderedDFA12 = orderedOR(dfa, dfa2)
orderedDFA = orderedOR(dfa3,dfa2)
orderedDFA2 = generalized_orderedOR(orderedDFA, dfa)
conj_wdfa = prioritized_conj(wdfa3, wdfa2)
conj_wdfa.trim()
orderedDFA.show_diagram(path='./orderedDFA.png')
orderedDFA2.show_diagram(path='./orderedDFA2.png')
conj_wdfa.show_diagram(path='./conj_wdfa.png')
disj_wdfa  = prioritized_disj(wdfa3,wdfa2)
disj_wdfa.show_diagram(path='./disj_wdfa.png')


