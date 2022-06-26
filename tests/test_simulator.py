from conftest import construct_mdp, mdp_policy

from simulation.simulator import Simulator


def test_mdp_simulation(construct_mdp, mdp_policy):
    mdp = construct_mdp
    policy = mdp_policy
    simulator = Simulator(mdp=mdp, policy=policy, target=(1, 0))
    simulator.simulate()

    last_state = simulator.visualizable_trajectory[-1]
    try:
        assert last_state in mdp.obstacles or last_state == (1, 0)
    except:
        raise ValueError(simulator.visualizable_trajectory)


def test_product_mdp_simulation(construct_product_mdp, product_mdp_policy):
    mdp = construct_product_mdp
    policy = product_mdp_policy

    simulator = Simulator(mdp=mdp, policy=policy)
    simulator.simulate()

    last_state = simulator.visualizable_trajectory[-1]
    try:
        assert last_state in mdp._mdp.obstacles or last_state == (1, 6)
    except:
        raise ValueError(simulator.visualizable_trajectory)
