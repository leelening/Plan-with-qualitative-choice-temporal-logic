from numpy.testing import assert_array_equal
import numpy as np
import pytest


def test_product_mdp_transition(construct_product_mdp):
    product_mdp = construct_product_mdp
    assert "sT" in product_mdp.states and "sT" in product_mdp.transitions
    assert "aT" in product_mdp.actlist
    for s in product_mdp.transitions:
        assert "aT" in product_mdp.transitions[s]
        for a in product_mdp.transitions[s]:
            sum_probs = np.sum(
                product_mdp.transitions[s][a][ns]
                for ns in product_mdp.transitions[s][a]
            )
            assert_array_equal(
                sum_probs,
                1,
            )


TEST_CASE = (
    (((1, 0), "0"), "aT", "sT", 1),
    (((2, 0), "0"), "aT", "sT", 1),
    (((1, 3), "0"), "aT", "sT", 1),
    (((1, 1), "0"), 0, ((1, 2), "0"), 0.8),
)


@pytest.mark.parametrize("s, a, ns, p", TEST_CASE)
def test_product_mdp_transition_matrix(construct_product_mdp, s, a, ns, p):
    product_mdp = construct_product_mdp
    try:
        assert_array_equal(product_mdp.transitions[s][a][ns], p)
    except Exception:
        raise ValueError(product_mdp.transitions[s][a])
