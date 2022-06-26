from mdp.mdp import MDP


class Simulator(object):
    def __init__(self, mdp: MDP, policy: dict, target=None) -> None:
        self.mdp = mdp
        self.target = target
        self.policy = policy

        self.visualizable_trajectory = []

    def simulate(self):
        if hasattr(self.mdp, "_wdfa"):
            self.simulate_product_mdp()
        else:
            self.simulate_mdp()

    def simulate_mdp(self):
        s = self.mdp.init
        while not (
            (s == "sink")
            or (s is self.mdp.obstacles)
            or (self.target and s == self.target)
        ):
            self.visualizable_trajectory.append(s)
            s = self.mdp.stochastic_transition(s, self.policy[s])
        self.visualizable_trajectory.append(s)
