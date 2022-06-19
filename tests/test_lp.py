import pytest

from solver.lp_solver import LPSolver

LP_TEST_CASE_1 = (((4, 1), 2), ((1, 2), 2), ((5, 4), 2), ((2, 1), 2))

LP_TEST_CASE_2 = (((2, 6), 3), ((0, 5), 0), ((0, 6), 1), ((7, 6), 3))


@pytest.mark.parametrize("s, a", LP_TEST_CASE_1)
def test_lp_1(construct_mdp_with_reward_1, s, a):
    lp_solver = LPSolver(construct_mdp_with_reward_1)

    lp_solver.solve()

    assert lp_solver.policy[s] == a
    assert lp_solver.value[s] > 0


@pytest.mark.parametrize("s, a", LP_TEST_CASE_2)
def test_lp_2(construct_mdp_with_reward_2, s, a):
    lp_solver = LPSolver(construct_mdp_with_reward_2)

    lp_solver.solve()

    assert lp_solver.policy[s] == a
    assert lp_solver.value[s] > 0
