__authors__ = ["Jie Fu", "Lening Li"]
__emails__ = ["fujie@ufl.edu", "lli4@wpi.edu"]
__copyright__ = "Copyright 2022, The Qualitative Logic + Temporal Logic Project"
__date__ = "2022-03-12"
__license__ = "GPL"
__version__ = "0.0.1"
__description__ = (
    "the code can be further improved:"
    "- the computation of the generalized ordered OR."
    "- the computation of product does include unreachable states. should use a better "
    "implementation that only generates states reachable from the initial state."
)
__status__ = "Production"

from automata.fa.dfa import DFA
from pydot import Dot, Edge, Node
import copy
from itertools import product
from collections import defaultdict
from typing import Optional


class WDFA(DFA):
    """
    A weighted deterministic finite-state automaton defined by
     1. a set of states,
     2. a set of input_symbols, that is, a set of atomic propositions
     3. transition model --- the deterministic transition function implemented as a dictionary: transitions[q][a]
        defines the next state going from state q with input a.
     4. an initial state,
     5. a set final states
     6. weight function, implemented as a dictionary: weight[q, a, nq] defines the weight going from state q to state nq
        with input a.
    """

    def __init__(
        self,
        states,
        input_symbols,
        transitions,
        initial_state,
        final_states,
        weight=None,
    ) -> None:
        # if the weight is None, we initialize transitions with all 0s.
        if weight is None:
            self.weight = {
                (q, a, nq): 0 for q, a, nq in product(states, input_symbols, states)
            }
        else:
            self.weight = copy.deepcopy(weight)
        # call the super class's initialization. NOTE: it contains super class's validate function
        super(WDFA, self).__init__(
            states=states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

    def get_transition(self, q, a) -> Optional[int]:
        return self.transitions[q][a] if a in self.transitions[q] else None

    def assign_weight(self, q, a, nq, weight) -> None:
        self.weight[q, a, nq] = weight

    def validate(self) -> None:
        """Validate all the weights are defined"""
        # call the dfa validate function
        super(WDFA, self).validate()
        # validate only weights
        for q, a in product(self.states, self.input_symbols):
            nq = self.get_transition(q, a)
            try:
                assert nq is not None
                # make sure the transitions are complete, which is not necessary
                # since super class' validate function is called.

                assert (
                    q,
                    a,
                    nq,
                ) in self.weight  # make sure the weights are defined completely.
            except Exception:
                print(
                    "Weight is not defined for state: {}, input_symbol: {}, next_state: {},".format(
                        q, a, nq
                    )
                )
                exit(-1)

    def trim(self) -> None:
        """remove unreachable states"""
        # some initializations
        states = [self.initial_state]
        weight = defaultdict()
        transitions = defaultdict(dict)
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
                # only add states not visited
                if next_state in states:
                    pass
                else:
                    states.append(next_state)

        # end of the iteration
        self.transitions = transitions
        self.weight = weight
        self.states = set(states)

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
                        label="{}: {}".format(to_label, weight) if weight else to_label,
                    )
                )
        if path:
            graph.write_png(path)
        return graph

    def get_option(self) -> int:
        # by default, all formulas have at least one way to be satisfied.
        opt = 1
        for (q, a, nq) in self.weight:
            if self.weight[q, a, nq] > opt:
                opt = self.weight[q, a, nq]
        return opt


def sync_product(dfa1, dfa2) -> DFA:
    """
    Creates a new DFA which is the cross product of DFAs self and other
    with an empty set of final states. The state is a tuple: The difference from _cross_product
    """
    assert dfa1.input_symbols == dfa2.input_symbols
    new_states = {(a, b) for a, b in product(dfa1.states, dfa2.states)}
    new_transitions = defaultdict(dict)
    for (state_a, transitions_a), symbol, (state_b, transitions_b) in product(
        dfa1.transitions.items(), dfa1.input_symbols, dfa2.transitions.items()
    ):
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


def get_wdfa_from_dfa(dfa) -> WDFA:
    """Creates a WDFA given a DFA"""
    # from a given DFA, adding sink state and assign weights to new transitions.
    wdfa = WDFA(
        dfa.states,
        dfa.input_symbols,
        dfa.transitions,
        dfa.initial_state,
        dfa.final_states,
    )
    # add end symbol to the input symbols set
    wdfa.input_symbols.add("end")
    # add a unique sink state
    wdfa.states.add("sink")
    # let sink state transits to itself.
    wdfa.transitions["sink"] = {a: "sink" for a in wdfa.input_symbols}

    # now assign weights to transition.
    for q, a in product(wdfa.states, wdfa.input_symbols):
        nq = None
        # if input symbol is !end and q is not at the final state
        if a != "end" and q not in wdfa.final_states:
            nq = wdfa.get_transition(q, a)
            wdfa.assign_weight(q, a, nq, 0)
        # if input symbol is end and q is not at the final state. Note that q can be sink state
        elif a == "end" and q not in wdfa.final_states:
            nq = q
            wdfa.assign_weight(q, a, nq, 0)
        # if input symbol is !end and q is at the final state.
        elif a != "end" and q in wdfa.final_states:
            nq = q
            wdfa.assign_weight(q, a, nq, 0)
        # if input symbol is end and q is at the final state.
        elif a == "end" and q in wdfa.final_states:
            nq = "sink"
            wdfa.assign_weight(q, a, "sink", 1)
        else:
            ValueError("Error: Unknown!")
        # modify the transition
        assert nq is not None
        wdfa.transitions[q][a] = nq
    wdfa.validate()
    return wdfa


def ordered_or(dfa1, dfa2) -> WDFA:
    """
    ordered OR Operator
    :param automata.fa.dfa.DFA dfa1: top priority given by dfa1
    :param automata.fa.dfa.DFA dfa2: secondary outcome given by dfa2
    :return: use automata product to construct the weighted automaton for ordered OR.
    """
    prod_dfa = sync_product(dfa1, dfa2)
    prod_wdfa = WDFA(
        states=prod_dfa.states,
        input_symbols=prod_dfa.input_symbols,
        transitions=prod_dfa.transitions,
        initial_state=prod_dfa.initial_state,
        final_states=prod_dfa.final_states,
    )
    # we do not assign any final states in the WDFA
    assert len(prod_wdfa.final_states) == 0
    # add end symbol to the input symbols set
    prod_wdfa.input_symbols.add("end")
    # add a unique sink state
    prod_wdfa.states.add("sink")

    # define the weight function and transition function
    for q, a in product(prod_wdfa.states, prod_wdfa.input_symbols):
        # add end symbol to the transitions
        if not prod_wdfa.get_transition(q, a):
            prod_wdfa.transitions[q][a] = q
            prod_wdfa.assign_weight(q, a, q, 0)
        # old transitions
        if q != "sink":
            (q1, q2) = q
            # prioritize dfa1 over dfa2
            if q1 in dfa1.final_states:
                prod_wdfa.transitions[q]["end"] = "sink"
                prod_wdfa.assign_weight(q, "end", "sink", 1)
            elif q2 in dfa2.final_states:
                prod_wdfa.transitions[q]["end"] = "sink"
                prod_wdfa.assign_weight(q, "end", "sink", 2)
    prod_wdfa.validate()
    return prod_wdfa


def generalized_ordered_or(wdfa, dfa) -> WDFA:
    """
    adding a new DFA, whose satisfaction is the least preferred.
    """
    assert isinstance(wdfa, WDFA)
    assert len(wdfa.final_states) == 0
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
        final_states=wdfa.final_states,
    )
    # validate explicitly
    dfa1.validate()
    prod_dfa = sync_product(dfa1, dfa)
    prod_wdfa = WDFA(
        states=prod_dfa.states,
        input_symbols=prod_dfa.input_symbols,
        transitions=prod_dfa.transitions,
        initial_state=prod_dfa.initial_state,
        final_states=prod_dfa.final_states,
    )
    assert len(prod_wdfa.final_states) == 0
    # add end symbol to the input symbols set
    prod_wdfa.input_symbols.add("end")
    # add a unique sink state
    prod_wdfa.states.add("sink")

    # define the weight function and transition function
    for q, a in product(prod_wdfa.states, prod_wdfa.input_symbols):
        # add end symbol to the transitions
        if not prod_wdfa.get_transition(q, a):
            prod_wdfa.transitions[q][a] = q
            prod_wdfa.assign_weight(q, a, q, 0)
        # old transitions
        if q != "sink":
            q1, q2 = q
            # prioritize dfa1 over dfa2
            nq1 = wdfa.transitions[q1][a]
            # satisfying the wdfa to a degree of satisfaction. NOTE: we do not use final_states here
            # due to generalization, that is, wdfa does not have final states.
            if nq1 == "sink":
                prod_wdfa.transitions[q]["end"] = "sink"
                prod_wdfa.assign_weight(q, "end", "sink", wdfa.get_option())
            # does not satisfy the original wdfa but satisfy the new least preferred outcome.
            elif q2 in dfa.final_states:
                prod_wdfa.transitions[q]["end"] = "sink"
                prod_wdfa.assign_weight(q, "end", "sink", wdfa.get_option() + 1)
    prod_wdfa.validate()
    return prod_wdfa


def prioritized_conj(wdfa1, wdfa2) -> WDFA:
    """
    prioritized conjunction: wdfa1 is preferred to wdfa2.
    """
    assert wdfa1.input_symbols == wdfa2.input_symbols
    # a list of product states without, (sink, x) or (x, sink) or (sink, sink), where x can be any state in Q.
    states = [
        (q1, q2)
        for q1, q2 in product(wdfa1.states, wdfa2.states)
        if q1 != "sink" and q2 != "sink"
    ]

    transitions = defaultdict(dict)
    transitions["sink"] = {a: "sink" for a in wdfa1.input_symbols}

    weight = {("sink", a, "sink"): 0 for a in wdfa1.input_symbols}

    opt2 = wdfa2.get_option()
    initial_state = (wdfa1.initial_state, wdfa2.initial_state)

    # define the weight function and transition function.
    for (q1, q2) in states:
        from_state = (q1, q2)
        # handle the normal product transitions
        for a in wdfa1.input_symbols:
            if a != "end":
                nq1 = wdfa1.transitions[q1][a]
                nq2 = wdfa2.transitions[q2][a]
                if nq1 != "sink" and nq2 != "sink":
                    to_state = (nq1, nq2)
                    transitions[from_state][a] = to_state
                    weight[(from_state, a, to_state)] = 0

        # initialize, these transition and weight can be modified later based on conditions,
        # but we added there for completeness.
        transitions[from_state]["end"] = from_state
        weight[(from_state, "end", from_state)] = 0
        if (
            "end" in wdfa1.transitions[q1]
            and "sink" == wdfa1.transitions[q1]["end"]
            and "end" in wdfa2.transitions[q2]
            and "sink" == wdfa2.transitions[q2]["end"]
        ):
            # both states are accepting to certain degree.
            transitions[from_state]["end"] = "sink"
            sat1 = wdfa1.weight[q1, "end", "sink"]
            sat2 = wdfa2.weight[q2, "end", "sink"]
            weight[(from_state, "end", "sink")] = opt2 * (sat1 - 1) + sat2
    # add the sink state into the stats
    states.append("sink")

    conj_wdfa = WDFA(
        states=set(states),
        input_symbols=wdfa1.input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=set(),
        weight=weight,
    )
    conj_wdfa.validate()
    return conj_wdfa


def prioritized_disj(wdfa1, wdfa2):
    """
    prioritized disjunction: wdfa1 is preferred over wdfa2
    """
    assert wdfa1.input_symbols == wdfa2.input_symbols
    # a list of product states without, (sink, x) or (x, sink) or (sink, sink), where x can be any state in Q.
    states = [
        (q1, q2)
        for q1, q2 in product(wdfa1.states, wdfa2.states)
        if q1 != "sink" and q2 != "sink"
    ]

    transitions = defaultdict(dict)
    transitions["sink"] = {a: "sink" for a in wdfa1.input_symbols}

    weight = {("sink", a, "sink"): 0 for a in wdfa1.input_symbols}

    opt2 = wdfa2.get_option()
    initial_state = (wdfa1.initial_state, wdfa2.initial_state)

    # define the weight function and transition function.
    for q1, q2 in states:
        from_state = (q1, q2)
        # handle the normal product transitions
        for a in wdfa1.input_symbols:
            if a != "end":
                nq1 = wdfa1.transitions[q1][a]
                nq2 = wdfa2.transitions[q2][a]
                to_state = (nq1, nq2)
                transitions[from_state][a] = to_state
                weight[(from_state, a, to_state)] = 0

        # initialize, these transition and weight can be modified later based on conditions,
        # but we added there for completeness.
        transitions[from_state]["end"] = from_state
        weight[(from_state, "end", from_state)] = 0
        if (
            "end" in wdfa1.transitions[q1]
            and "sink" in wdfa1.transitions[q1]["end"]
            and wdfa1.weight[(q1, "end", "sink")] == 1
        ) or (
            "end" in wdfa2.transitions[q2]
            and "sink" in wdfa2.transitions[q2]["end"]
            and wdfa2.weight[(q2, "end", "sink")] == 1
        ):
            transitions[from_state]["end"] = "sink"
            weight[(from_state, "end", "sink")] = 1
        if (
            "end" in wdfa1.transitions[q1]
            and "sink" in wdfa1.transitions[q1]["end"]
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
                and "sink" in wdfa1.transitions[q1]["end"]
                and wdfa1.weight[(q1, "end", "sink")] > 1
            )
            or "end" not in wdfa1.transitions[q1]
        ) and (
            "end" in wdfa2.transitions[q2]
            and "sink" in wdfa2.transitions[q2]["end"]
            and wdfa2.weight[(q2, "end", "sink")] > 1
        ):
            transitions[from_state]["end"] = "sink"
            weight[(from_state, "end", "sink")] = wdfa2.weight[(q2, "end", "sink")]

    # add the sink state into the stats
    states.append("sink")
    disj_wdfa = WDFA(
        states=set(states),
        input_symbols=wdfa1.input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=set(),
        weight=weight,
    )
    disj_wdfa.validate()
    return disj_wdfa


if __name__ == "__main__":
    print("to add main")
