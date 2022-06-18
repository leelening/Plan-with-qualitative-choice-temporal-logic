from automata.fa.dfa import DFA
from collections import defaultdict
from itertools import product

from wdfa.wdfa import WDFA


def get_wdfa_from_dfa(dfa: DFA) -> WDFA:
    """
    Return a wdfa from a given dfa

    :param dfa: given a dfa
    :return: the converted wdfa
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


def sync_product(dfa1: DFA, dfa2: DFA) -> DFA:
    """
    Creates a new DFA which is the cross product of DFAs self and other
    with an empty set of final states. The state is a tuple: The difference from _cross_product

    :param dfa1: The first dfa
    :param dfa2: The second dfa
    :return: A new DFA
    """
    try:
        assert dfa1.input_symbols == dfa2.input_symbols
    except AssertionError:
        raise ValueError("The input labels of these two DFAs are different.")

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


def ordered_or(dfa1: DFA, dfa2: DFA) -> WDFA:
    """
    ordered OR Operator

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
    # opt(varphi1) + opt(varphi2)
    prod_wdfa.set_option(2)
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
                prod_wdfa.assign_weight(
                    q,
                    "end",
                    "sink",
                    min(
                        wdfa.weight[q1, "end", nq1],
                        prod_wdfa.weight.get((q, "end", "sink"), 100),
                    ),
                )
            # does not satisfy the original wdfa but satisfy the new least preferred outcome.
            elif q2 in dfa.final_states:
                prod_wdfa.transitions[q]["end"] = "sink"
                prod_wdfa.assign_weight(
                    q,
                    "end",
                    "sink",
                    min(
                        wdfa.get_option() + 1,
                        prod_wdfa.weight.get((q, "end", "sink"), 100),
                    ),
                )
    # opt(varphi1) + opt(varphi2)
    prod_wdfa.set_option(wdfa.get_option() + 1)
    prod_wdfa.validate()
    return prod_wdfa


def prioritized_conj(wdfa1, wdfa2) -> WDFA:
    """
    prioritized conjunction: wdfa1 is preferred to wdfa2.
    """
    if wdfa1.input_symbols != wdfa2.input_symbols:
        wdfa1.input_symbols.update(wdfa2.input_symbols)
    diff = wdfa1.input_symbols - wdfa2.input_symbols
    for q2 in wdfa2.transitions:
        for a in diff:
            wdfa2.transitions[q2][a] = q2
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
    # opt(varphi1) * opt(varphi2)
    conj_wdfa.set_option(wdfa1.get_option() * wdfa2.get_option())
    conj_wdfa.validate()
    return conj_wdfa
