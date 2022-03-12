__author__ = "Jie Fu and Lening Li"
__email__ = "fujie@ufl.edu and lli4@wpi.edu"
__version__ = "0.0.1"
__maintainer__ = "Jie Fu and Lening Li"
__description__ = (
    "the code can be further improved:"
    "- the computation of the generalized ordered OR."
    "- the computation of product does include unreachable states. should use a better "
    "implementation that only generates states reachable from the initial state."
)

from automata.fa.dfa import DFA
from pydot import Dot, Edge, Node
import copy
from itertools import product
from collections import defaultdict


class WDFA(DFA):
    """
    A weighted deterministic finite-state automaton defined by
     1. a set of states,
     2. a set of input_symbols, that is, a set of atomic propositions
     3. transition model --- the deterministic transition function implemented as a dictionary: transitions[q][a] defines the next state going from state q with input a.
     4. an initial state,
     5. a set final states
     6. weight function, implemented as a dictionary: weight[q, a, nq] defines the weight going from state q to state nq with input a.
    """

    def __init__(
        self,
        states,
        input_symbols,
        transitions,
        initial_state,
        final_states,
        weight=None,
    ):
        if weight is None:
            self.weight = {
                (q, a, nq): 0 for q in states for a in input_symbols for nq in states
            }
        else:
            self.weight = copy.deepcopy(weight)
        super(WDFA, self).__init__(
            states=states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

    def get_transition(self, q, a):
        try:
            self.transitions[q][a]
        except Exception:
            print(
                "Error! Transition is not defined for state: {}, inputSymbol: {}".format(
                    q, a
                )
            )

    def validate(self):
        """Validate all the weights are defined"""
        # call the dfa validate function
        super(WDFA, self).validate()
        for q, a in product(self.states, self.input_symbols):
            nq = self.transitions[q][a]
            try:
                assert (q, a, nq) in self.weight
            except Exception:
                print(
                    "Weight is not defined for state: {}, input_symbol: {}, next_state: {},".format(
                        q, a, nq
                    )
                )

    def add_weight(self, q, a, nq, weight):
        self.weight[q, a, nq] = weight

    def trim(self):
        """
        remove unreachable states
        :return:
        """
        states = [self.initial_state]  # visited states
        weight = defaultdict()
        transitions = defaultdict(defaultdict)
        count = 0
        # iteratively trim the automaton
        while count < len(states):
            from_state = states[count]
            count = count + 1  # move the pointer to the next state.
            # count is the number of reachable states.
            for a in self.transitions[from_state]:
                next_state = self.transitions[from_state][a]
                transitions[from_state][a] = next_state
                weight[from_state, a, next_state] = self.weight[
                    from_state, a, next_state
                ]
                if next_state in states:
                    pass
                else:
                    states.append(next_state)

        # end of the iteration
        self.transitions = transitions
        self.weight = weight
        self.states = set(states)
        return

    def show_diagram(self, path=None):  # pragma: no cover
        """
        Creates the graph associated with this DFA
        """
        # Nodes are set of states
        graph = Dot(graph_type="digraph", rankdir="LR")
        nodes = {}
        for state in self.states:
            if state == self.initial_state:
                # color start state with green
                if state in self.final_states:
                    initial_state_node = Node(
                        str(state), style="filled", peripheries=2, fillcolor="#66cc33"
                    )
                else:
                    initial_state_node = Node(
                        str(state), style="filled", fillcolor="#66cc33"
                    )
                nodes[str(state)] = initial_state_node
                graph.add_node(initial_state_node)
            else:
                if state in self.final_states:
                    state_node = Node(str(state), peripheries=2)
                else:
                    state_node = Node(str(state))
                nodes[str(state)] = state_node
                graph.add_node(state_node)
        # adding edges
        for from_state, lookup in self.transitions.items():
            # omit all self-loop at the sink state.
            for to_label, to_state in lookup.items():
                if (from_state, to_label, to_state) in self.weight:
                    weight = self.weight[from_state, to_label, to_state]
                else:
                    weight = 0
                graph.add_edge(
                    Edge(
                        nodes[str(from_state)],
                        nodes[str(to_state)],
                        label=to_label + str(weight),
                    )
                )
        if path:
            graph.write_png(path)
        return graph

    def get_option(self):
        opt = 1  # by default, all formulas have at least one way to be satisfied.
        for (q, a, nq) in self.weight:
            if self.weight[q, a, nq] > opt:
                opt = self.weight[(q, a, nq)]
        return opt


def sync_product(dfa1, dfa2):
    """
    Creates a new DFA which is the cross product of DFAs self and other
    with an empty set of final states. The state is a tuple: The difference from _cross_product
    """
    assert dfa1.input_symbols == dfa2.input_symbols
    new_states = {(a, b) for a, b in product(dfa1.states, dfa2.states)}
    new_transitions = defaultdict(defaultdict)
    for (state_a, transitions_a), (state_b, transitions_b) in product(
        dfa1.transitions.items(), dfa2.transitions.items()
    ):
        for symbol in dfa1.input_symbols:
            new_transitions[state_a, state_b][symbol] = (
                transitions_a[symbol],
                transitions_b[symbol],
            )
    new_initial_state = (dfa1.initial_state, dfa2.initial_state)
    return DFA(
        states=new_states,
        input_symbols=dfa1.input_symbols,
        transitions=new_transitions,
        initial_state=new_initial_state,
        final_states=set(),
    )


def get_wdfa_from_dfa(dfa):
    """Creates a WDFA given a DFA"""
    # from a given DFA, adding sink state and assign weights to new transitions.
    wdfa = WDFA(
        dfa.states,
        dfa.input_symbols,
        dfa.transitions,
        dfa.initial_state,
        dfa.final_states,
    )
    wdfa.input_symbols.add("end")
    wdfa.states.add("sink")  # and unique sink states
    wdfa.transitions["sink"] = {a: "sink" for a in wdfa.input_symbols}

    # now assign weights to transition.
    for q, a in product(wdfa.states, wdfa.input_symbols):
        if a != "end" and q not in wdfa.final_states:
            nq = wdfa.get_transition(q, a)
            wdfa.add_weight(q, a, nq, 0)
        elif a == "end" and q not in wdfa.final_states:
            nq = q
            wdfa.add_weight(q, a, nq, 0)
        elif a != "end" and q in wdfa.final_states:
            nq = q
            wdfa.add_weight(q, a, nq, 0)
        elif a == "end" and q in wdfa.final_states:
            nq = "sink"
            wdfa.add_weight(q, a, "sink", 1)
        else:
            ValueError("Error: Unknown!")
        wdfa.transitions[q][a] = nq
    wdfa.validate()
    return wdfa


def orderedOR(dfa1, dfa2):
    """
    :param dfa1: top priority given by dfa1
    :param dfa2: secondary outcome given by dfa2
    :return: use automata product to construct the weighted automaton for ordered OR.
    """
    prod_dfa = sync_product(dfa1, dfa2)
    prod_wdfa = WDFA(
        states=prod_dfa.states,
        input_symbols=prod_dfa.input_symbols,
        transitions=prod_dfa.transitions,
        initial_state=prod_dfa.initial_state,
        final_states=prod_dfa.final_states,
        weight={},
    )
    prod_wdfa.input_symbols.add("end")  # include the ending of the string symbol.
    prod_wdfa.states.add("sink")  # adding the unique sink state.
    # define the weight function
    for q, a in product(prod_wdfa.states, prod_wdfa.input_symbols):
        if not prod_wdfa.get_transition(q, a):
            prod_wdfa.transitions[q][a] = q
            prod_wdfa.add_weight(q, a, q, 0)
        if q != "sink":
            (q1, q2) = q
            if q1 in dfa1.final_states:
                prod_wdfa.transitions[q]["end"] = "sink"
                prod_wdfa.add_weight(q, "end", "sink", 1)
            elif q2 in dfa2.final_states:
                prod_wdfa.transitions[q]["end"] = "sink"
                prod_wdfa.add_weight(q, "end", "sink", 2)
    prod_wdfa.validate()
    return prod_wdfa


def generalized_orderedOR(wdfa, dfa):
    """
     adding a new DFA, whose satisfaction is the least preferred. The implementation is functional but not ideal. NEED REVISION.
    :param wdfa:
    :param dfa:
    :return:
    """
    # TODO: finish working there
    assert isinstance(wdfa, WDFA)
    assert isinstance(dfa, DFA)
    # construct a DFA from the weighted DFA by removing the transitions labeled with 'end' and reaching sink state.
    dfa_states = wdfa.states - {"sink"}
    dfa_input_symbols = wdfa.input_symbols - {"end"}
    dfa_transitions = {
        q: {a: wdfa.transitions[q][a] for a in dfa_input_symbols} for q in dfa_states
    }
    dfa1 = DFA(
        states=dfa_states,
        input_symbols=dfa_input_symbols,
        transitions=dfa_transitions,
        initial_state=wdfa.initial_state,
        final_states=set(),
    )
    temp = sync_product(dfa1, dfa)
    prod_wdfa = WDFA(
        states=temp.states,
        input_symbols=temp.input_symbols,
        transitions=temp.transitions,
        initial_state=temp.initial_state,
        final_states=temp.final_states,
        weight={},
    )
    prod_wdfa.states.add("sink")  # adding the unique sink state.
    prod_wdfa.input_symbols.add("end")
    prod_wdfa.transitions["sink"] = {}  # adding dict for transitions from sink state.
    # to determine the maximal degree of satisfaction (dos) in the given wdfa
    maxdos = 1  # by default, the dos can only be greater than one
    # find the largest dos
    for q1 in wdfa.states:
        for a in wdfa.transitions[q1]:
            nq1 = wdfa.transitions[q1][a]
            if wdfa.weight[(q1, a, nq1)] > maxdos:
                maxdos = wdfa.weight[(q1, a, nq1)]

    for q, a in product(prod_wdfa.states, prod_wdfa.input_symbols):
        if not prod_wdfa.get_transition(q, a):
            prod_wdfa.transitions[q][a] = q
            prod_wdfa.add_weight(q, a, q, 0)
        if q != "sink":
            q1, q2 = q
            nq1 = wdfa.transitions[q1][a]
            if nq1 == "sink":  # satisfying the wdfa to a degree of satisfaction.
                prod_wdfa.transitions[q]["end"] = "sink"
                prod_wdfa.add_weight(q, "end", "sink", wdfa.weight[(q1, "end", nq1)])
            if a != "end":
                nq2 = dfa.transitions[q2][a]
                if (
                    nq2 in dfa.final_states
                ):  # does not satisfy the original wdfa but satisfy the new least preferred outcome.
                    prod_wdfa.transitions[q]["end"] = "sink"
                    prod_wdfa.add_weight(q, "end", "sink", maxdos + 1)
    prod_wdfa.validate()
    return prod_wdfa


def prioritized_conj(wdfa1, wdfa2):
    """
    :param wdfa1: first formula
    :param wdfa2: second formula
    :return: wdfa for wdfa1 land wdfa2 where land is prioritized conjunction: wdfa1 is preferred to wdfa2.
    """
    # TODO: stop here.
    states = {"sink"}
    transitions = defaultdict(defaultdict)
    weight = defaultdict()
    opt2 = wdfa2.get_option()
    init = (wdfa1.initial_state, wdfa2.initial_state)
    for q1, q2 in product(wdfa1.states, wdfa2.states):
        if q1 != "sink" and q2 != "sink":
            from_state = (q1, q2)
            states.add(from_state)
            for a in wdfa1.input_symbols:
                if a != "end":
                    nq1 = wdfa1.transitions[q1][a]
                    nq2 = wdfa2.transitions[q2][a]
                    to_state = (nq1, nq2)
                    states.add(to_state)
                    transitions[from_state][a] = to_state
                    weight[(from_state, a, to_state)] = 0
            if "end" in wdfa1.transitions[q1] and "end" in wdfa2.transitions[q2]:
                # both states are accepting to certain degree.
                transitions[from_state]["end"] = "sink"
                sat1 = wdfa1.weight[(q1, "end", "sink")]
                sat2 = wdfa2.weight[(q2, "end", "sink")]
                weight[(from_state, "end", "sink")] = opt2 * (sat1 - 1) + sat2
    transitions["sink"] = defaultdict(defaultdict)
    for a in wdfa1.input_symbols:
        transitions["sink"][a] = "sink"
        weight[("sink", a, "sink")] = 0
    conj_wdfa = WDFA(states, wdfa1.input_symbols, transitions, init, set([]), weight)
    conj_wdfa.validate()
    return conj_wdfa


def prioritized_disj(wdfa1, wdfa2):
    """
    :param wdfa1:
    :param wdfa2:
    :return:
    """
    states = set(["sink"])
    transitions = dict([])
    weight = dict([])
    opt2 = wdfa2.get_option()
    init = (wdfa1.initial_state, wdfa2.initial_state)
    for q1 in wdfa1.states:
        for q2 in wdfa2.states:
            if q1 != "sink" and q2 != "sink":
                from_state = (q1, q2)
                states.add(from_state)
                transitions[from_state] = dict([])
                for a in wdfa1.input_symbols:
                    if a != "end":
                        nq1 = wdfa1.transitions[q1][a]
                        nq2 = wdfa2.transitions[q2][a]
                        to_state = (nq1, nq2)
                        states.add(to_state)
                        transitions[from_state][a] = to_state
                        weight[(from_state, a, to_state)] = 0
                if (
                    "end" in wdfa1.transitions[q1]
                    and wdfa1.weight[(q1, "end", "sink")] == 1
                ) or (
                    "end" in wdfa2.transitions[q2]
                    and wdfa2.weight[(q2, "end", "sink")] == 1
                ):

                    transitions[from_state]["end"] = "sink"
                    weight[(from_state, "end", "sink")] = 1
                if (
                    "end" in wdfa1.transitions[q1]
                    and wdfa1.weight[(q1, "end", "sink")] > 1
                    and "end" not in wdfa2.transitions[q2]
                ):
                    transitions[from_state]["end"] = "sink"
                    weight[(from_state, "end", "sink")] = (
                        opt2 * (wdfa1.weight[(q1, "end", "sink")] - 1) + 1
                    )
                if (
                    (
                        "end" in wdfa1.transitions[q1]
                        and wdfa1.weight[(q1, "end", "sink")] > 1
                    )
                    or "end" not in wdfa1.transitions[q1]
                ) and (
                    "end" in wdfa2.transitions[q2]
                    and wdfa2.weight[(q2, "end", "sink")] > 1
                ):
                    transitions[from_state]["end"] = "sink"
                    weight[(from_state, "end", "sink")] = wdfa2.weight[
                        (q2, "end", "sink")
                    ]
    transitions["sink"] = dict([])
    for a in wdfa1.input_symbols:
        transitions["sink"][a] = "sink"
        weight[("sink", a, "sink")] = 0
    disj_wdfa = WDFA(states, wdfa1.input_symbols, transitions, init, set([]), weight)
    disj_wdfa.validate()
    return disj_wdfa


if __name__ == "__main__":
    print("to add main")
