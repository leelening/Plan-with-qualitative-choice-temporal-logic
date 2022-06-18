import pytest
from wdfa.helpers import sync
from wdfa.helpers import ordered_or, prioritized_conj

ORDERED_OR_TEST_CASE = (
    (("0", "0"), "E", ("0", "0"), 0),
    (
        ("0", "0"),
        "a",
        ("1", "0"),
        0,
    ),
    (("1", "1"), "end", "sink", 1),
    (("0", "1"), "end", "sink", 2),
    (("1", "0"), "end", "sink", 1),
    ("sink", "end", "sink", 0),
    ("sink", "a", "sink", 0),
)

PRIORITIZED_CONJ_TEST_CASE = (
    (("1", "1"), "end", "sink", 1),
    (("2", "1"), "end", "sink", 0),
)


def test_set_options(get_wdfa_from_eventually_a_dfa):
    wdfa = get_wdfa_from_eventually_a_dfa
    wdfa.set_option(10)
    wdfa.validate()
    assert wdfa.opt == 10


def test_sync(get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa):
    sync_wdfa = sync(get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa)
    print(sync_wdfa)
    sync_wdfa.validate()


@pytest.mark.parametrize("q, a, nq, w", ORDERED_OR_TEST_CASE)
def test_ordered_or(
    get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa, q, a, nq, w
):
    wdfa = ordered_or(get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa)
    print(get_wdfa_from_eventually_a_dfa)
    assert wdfa.weight[q, a, nq] == w


@pytest.mark.parametrize("q, a, nq, w", PRIORITIZED_CONJ_TEST_CASE)
def test_prioritized_conj(
    get_wdfa_from_not_a_until_b_dfa, get_wdfa_from_eventually_a_dfa, q, a, nq, w
):
    wdfa = prioritized_conj(
        get_wdfa_from_not_a_until_b_dfa, get_wdfa_from_eventually_a_dfa
    )
    assert wdfa.weight[q, a, nq] == w
