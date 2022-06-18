from hashlib import new
from tkinter import W
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


def ordered_or(wdfa1: WDFA, wdfa2: WDFA) -> WDFA:
    """
    ordered OR Operator

    :param wdfa1: top priority given by wdfa1
    :param wdfa2: secondary outcome given by wdfa2
    :return: use automata product to construct the weighted automaton for ordered OR.
    """
    prod_wdfa = sync_or(wdfa1, wdfa2)
    assert len(prod_wdfa.final_states) == 0

    for q in prod_wdfa.states:
        if q != "sink":
            prod_wdfa.transitions[q]["end"] = "sink"
            (q1, q2) = q

            if (
                wdfa1.weight[q1, "end", "sink"] == 0
                and wdfa2.weight[q2, "end", "sink"] == 0
            ):
                prod_wdfa.assign_weight(q, "end", "sink", 0)
            elif (
                wdfa1.weight[q1, "end", "sink"] == 0
                and wdfa2.weight[q2, "end", "sink"] > 0
            ):
                prod_wdfa.assign_weight(
                    q,
                    "end",
                    "sink",
                    wdfa2.weight[q2, "end", "sink"] + wdfa1.opt,
                )

            elif (
                wdfa1.weight[q1, "end", "sink"] > 0
                and wdfa2.weight[q2, "end", "sink"] == 0
            ):
                prod_wdfa.assign_weight(q, "end", "sink", wdfa1.opt)

    prod_wdfa.set_option(wdfa1.opt + wdfa2.opt)
    prod_wdfa.validate()
    return prod_wdfa


def prioritized_conj(wdfa1: WDFA, wdfa2: WDFA) -> WDFA:
    """
    prioritized conjunction: wdfa1 is preferred to wdfa2.
    """
    conj_wdfa = sync_conj(wdfa1, wdfa2)

    for q in conj_wdfa.states:
        if q != "sink":
            (q1, q2) = q
            if (
                wdfa1.transition[q1]["end"] == "sink"
                and wdfa2.transition[q1]["end"] == "sink"
            ):
                conj_wdfa.transition[q]["end"] = "sink"

            elif (
                wdfa1.weight[q1, "end", "sink"] > 0
                and wdfa2.weight[q2, "end", "sink"] > 0
            ):
                conj_wdfa.weight[q, "end", "sink"] = (
                    wdfa1.weight[q1, "end", "sink"] * wdfa2.weight[q2, "end", "sink"]
                )
            elif (
                wdfa1.weight[q1, "end", "sink"] == 0
                and wdfa2.weight[q2, "end", "sink"] == 0
            ):
                conj_wdfa.weight[q, "end", "sink"] = 0

    conj_wdfa.validate()
    return conj_wdfa


def sync(wdfa1: WDFA, wdfa2: WDFA) -> WDFA:
    """
    Creates a new WDFA which is the cross product of DFAs self and other
    with an empty set of final states. The state is a tuple: The difference from _cross_product

    :param wdfa1: The first wdfa
    :param wdfa2: The second wdfa
    :return: A new DFA
    """
    try:
        assert wdfa1.input_symbols == wdfa2.input_symbols
    except AssertionError:
        raise ValueError("The input labels of these two DFAs are different.")

    new_states = {
        (a, b)
        for a, b in product(wdfa1.states, wdfa2.states)
        if not (a == "sink" or b == "sink")
    }

    new_transitions = defaultdict(dict)
    new_input_symbols = wdfa2.input_symbols
    new_input_symbols.remove("end")

    for (state_a, transitions_a), symbol, (state_b, transitions_b) in product(
        wdfa1.transitions.items(), new_input_symbols, wdfa2.transitions.items()
    ):
        if not (
            state_a == "sink"
            or state_b == "sink"
            or symbol == "end"
            or transitions_a[symbol] == "sink"
            or transitions_b[symbol] == "sink"
        ):
            new_transitions[state_a, state_b][symbol] = (
                transitions_a[symbol],
                transitions_b[symbol],
            )
    new_initial_state = (wdfa1.initial_state, wdfa2.initial_state)

    wdfa = WDFA(
        states=new_states,
        input_symbols=new_input_symbols,
        transitions=new_transitions,
        initial_state=new_initial_state,
        final_states=set(),
    )
    wdfa.states.add("sink")
    wdfa.input_symbols.add("end")
    for a in wdfa.input_symbols:
        wdfa.assign_weight("sink", a, "sink", 0)
        wdfa.transitions["sink"][a] = "sink"
    for q in wdfa.states:
        wdfa.transitions[q]["end"] = "sink"
        wdfa.assign_weight(q, "end", "sink", 0)
    return wdfa


def sync_conj(wdfa1: WDFA, wdfa2: WDFA) -> WDFA:
    wdfa = sync(wdfa1, wdfa2)
    wdfa.set_option(wdfa1.opt * wdfa2.opt)
    return wdfa


def sync_or(wdfa1: WDFA, wdfa2: WDFA) -> WDFA:
    wdfa = sync(wdfa1, wdfa2)
    wdfa.set_option(wdfa1.opt + wdfa2.opt)
    return wdfa
