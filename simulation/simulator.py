from mdp.mdp import MDP


class Simulator(object):
    def __init__(self, mdp: MDP, policy: dict, target=None) -> None:
        """
        Initialize a simulator for the MDP

        :param mdp: MDP or product mdp
        :param policy: the policy
        :type policy: dict
        :param target: the target of the MDP, defaults to None
        """
        self.mdp = mdp
        self.target = target
        self.policy = policy

        self.visualizable_trajectory = []

        self.trajectories = []

    def simulate(self):
        """
        If the mdp is pure mdp, then run simulate_mdp,
        else run simulation_product_mdp
        """
        if hasattr(self.mdp, "_wdfa"):
            self.simulate_product_mdp()
        else:
            if not self.target:
                raise ValueError("Did not set the target for the pure MDP!")
            self.simulate_mdp()

    def simulate_mdp(self):
        s = self.mdp.init
        while not (
            (s == "sT")
            or (s in self.mdp.obstacles)
            or (self.target and s == self.target)
        ):
            self.visualizable_trajectory.append(s)
            s = self.mdp.stochastic_transition(s, self.policy[s])

        if s != "sT":
            self.visualizable_trajectory.append(s)

    def simulate_product_mdp(self):
        s = self.mdp.init
        while not (
            (s[0] == "sT")
            or (s[0] in self.mdp._mdp.obstacles)
            or (self.target and s == self.target)
        ):
            self.visualizable_trajectory.append(s[0])
            s = self.mdp.stochastic_transition(s, self.policy[s])
        if s[0] != "sT":
            self.visualizable_trajectory.append(s[0])

    def sample_trajectories(self, number: int = 1) -> list:
        """
        Simulate given numbers of trajectories.

        :param number: the number of trajectory, defaults to 1
        :return: the list of trajectories
        """
        for _ in range(number):
            self.visualizable_trajectory = []
            self.simulate()
            self.trajectories.append(self.visualizable_trajectory)
        return self.trajectories
