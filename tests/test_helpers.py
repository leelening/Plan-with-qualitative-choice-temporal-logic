import pytest
from wdfa.helpers import sync
from wdfa.helpers import ordered_or, prioritized_conj

ORDERED_OR_TEST_CASE_SIMPLE = (
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

ORDERED_OR_TEST_CASE_COMPLEX = (
    ((("1", "1"), "1"), "end", "sink", 1),
    ((("2", "1"), "1"), "end", "sink", 2),
)

PRIORITIZED_CONJ_TEST_CASE_SIMPLE = (
    (("1", "1"), "end", "sink", 1),
    (("2", "1"), "end", "sink", 0),
    (("0", "0"), "a", ("2", "1"), 0),
)


PRIORITIZED_CONJ_TEST_CASE_COMPLEX = (
    ((("1", "1"), ("1", "1")), "end", "sink", 1),
    ((("2", "1"), ("1", "1")), "end", "sink", 3),
    ((("2", "1"), ("1", "0")), "end", "sink", 3),
    ((("1", "0"), ("0", "1")), "end", "sink", 2),
    ((("1", "0"), ("0", "1")), "a", (("1", "1"), ("1", "1")), 0),
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


@pytest.mark.parametrize("q, a, nq, w", ORDERED_OR_TEST_CASE_SIMPLE)
def test_ordered_or_simple(
    get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa, q, a, nq, w
):
    wdfa = ordered_or(get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa)
    print(get_wdfa_from_eventually_a_dfa)
    assert wdfa.weight[q, a, nq] == w


@pytest.mark.parametrize("q, a, nq, w", ORDERED_OR_TEST_CASE_COMPLEX)
def test_ordered_or_complex(
    get_wdfa_from_not_a_until_b_dfa,
    get_wdfa_from_eventually_a_dfa,
    get_wdfa_from_eventually_b_dfa,
    q,
    a,
    nq,
    w,
):
    wdfa = ordered_or(get_wdfa_from_not_a_until_b_dfa, get_wdfa_from_eventually_a_dfa)
    wdfa = ordered_or(wdfa, get_wdfa_from_eventually_b_dfa)
    print(get_wdfa_from_eventually_a_dfa)
    assert wdfa.weight[q, a, nq] == w


@pytest.mark.parametrize("q, a, nq, w", PRIORITIZED_CONJ_TEST_CASE_SIMPLE)
def test_prioritized_conj_simple(
    get_wdfa_from_not_a_until_b_dfa, get_wdfa_from_eventually_a_dfa, q, a, nq, w
):
    wdfa = prioritized_conj(
        get_wdfa_from_not_a_until_b_dfa, get_wdfa_from_eventually_a_dfa
    )
    assert wdfa.weight[q, a, nq] == w


@pytest.mark.parametrize("q, a, nq, w", PRIORITIZED_CONJ_TEST_CASE_COMPLEX)
def test_prioritized_conj_complex(
    get_wdfa_from_not_a_until_b_dfa,
    get_wdfa_from_eventually_a_dfa,
    get_wdfa_from_eventually_b_dfa,
    q,
    a,
    nq,
    w,
):
    wdfa1 = ordered_or(get_wdfa_from_not_a_until_b_dfa, get_wdfa_from_eventually_a_dfa)
    wdfa2 = ordered_or(get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa)
    wdfa3 = prioritized_conj(wdfa1, wdfa2)
    assert wdfa3.weight[q, a, nq] == w
