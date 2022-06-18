from numpy.testing import assert_array_equal
import numpy as np


def test_product_mdp_transition(construct_product_mdp):
    product_mdp = construct_product_mdp
    for s in product_mdp.transitions:
        for a in product_mdp.transitions[a]:
            sum_probs = np.sum(
                product_mdp.transitions[s][a][ns]
                for ns in product_mdp.transitions[s][a]
            )
            assert_array_equal(
                sum_probs,
                1,
            )
