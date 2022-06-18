from automata.fa.dfa import DFA
from pydot import Dot, Edge, Node
from itertools import product
from collections import defaultdict


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
        if weight is None:
            self.weight = {
                (q, a, nq): 0 for q, a, nq in product(states, input_symbols, states)
            }
        else:
            self.weight = weight
        # call the super class's initialization. NOTE: it contains super class's validate function
        super(WDFA, self).__init__(
            states=states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
        )

    def assign_weight(self, q: str, a: str, nq: str, weight: float) -> None:
        """
        Assign the weight given the current automaton state, input label, next automaton state, and the weight.

        :param q: the current automaton state
        :param a: the current input label
        :param nq: the next automaton state
        :param weight: the weight
        """
        self.weight[q, a, nq] = weight

    def validate(self) -> None:
        """
        Validate the WDFA.
        """
        super(WDFA, self).validate()

        for q, a in product(self.states, self.input_symbols):
            nq = self.get_transition(q, a)
            try:
                assert nq is not None
                assert (
                    q,
                    a,
                    nq,
                ) in self.weight
            except AssertionError:
                raise ValueError(
                    "Weight is not defined for state: {}, input_symbol: {}, next_state: {},".format(
                        q, a, nq
                    )
                )

        try:
            assert hasattr(self, "opt")
        except AssertionError:
            raise ValueError(
                "This WDFA is not initialized completely. It does not have opt defined."
            )

    def trim(self) -> None:
        """
        Remove unreachable states
        """
        states = [self.initial_state]
        weight = defaultdict()
        transitions = defaultdict(dict)
        count = 0

        # iteratively trim the automaton
        while count < len(states):
            from_state = states[count]
            count += 1
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

        self.transitions = transitions
        self.weight = weight
        self.states = set(states)

    def show_diagram(self, path=None):
        """
        Creates the graph associated with this DFA
        :param path: the file path to save the diagram
        """
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

    def set_option(self, opt=1):
        self.opt = opt

    def get_option(self) -> int:
        return self.opt
