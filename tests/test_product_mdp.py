from numpy.testing import assert_array_equal
import numpy as np
from itertools import product


# def test_product_mdp_transition(construct_product_mdp):
#     product_mdp = construct_product_mdp

#     for s, a in product(product_mdp.states, product_mdp.actlist):
#         assert_array_equal(
#             np.sum(
#                 product_mdp.transitions[s][a][ns]
#                 for ns in product_mdp.transitions[s][a]
#             ),
#             1,
#         )
