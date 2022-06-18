from product_mdp.product_mdp import ProductMDP


def test_productmdp_constructor(construct_mdp, get_wdfa_from_eventually_a_dfa):
    product_mdp = ProductMDP(construct_mdp, get_wdfa_from_eventually_a_dfa)
    assert True
