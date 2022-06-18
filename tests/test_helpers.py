from wdfa.helpers import sync


def test_set_options(get_wdfa_from_eventually_a_dfa):
    wdfa = get_wdfa_from_eventually_a_dfa
    wdfa.set_option(10)
    wdfa.validate()
    assert wdfa.opt == 10


def test_sync(get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa):
    sync_dfa = sync(get_wdfa_from_eventually_a_dfa, get_wdfa_from_eventually_b_dfa)
    sync_dfa.validate()
