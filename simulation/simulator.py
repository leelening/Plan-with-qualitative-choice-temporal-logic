class Simulator(object):
    def __init__(self, mdp, policy) -> None:
        self.mdp = mdp
        self.policy = policy

    def 

    def simulate(self):
        current_state = self.mdp.init[0:2]
        while current_state[-1] != "sink":
            