import numpy as np

class Population:
    def __init__(self, N, I0):
        self.N = N
        self.agent_state = np.zeros(N)
        infected = np.random.choice(N, int(N*I0), replace=False)
        self.agent_state[infected] = 1
        self.agent_order = np.arange(N)

    def update(self, beta, mu):
        temp = self.agent_state.copy()
        for agent in np.random.permutation(self.agent_order):
            state = self.agent_state[agent]
            if state == 0:
                rnd_agent = np.random.choice([a for a in self.agent_order if a != agent])
                if self.agent_state[rnd_agent] == 1 and np.random.random() < beta:
                    temp[agent] = 1
            elif state == 1:
                if np.random.random() < mu:
                    temp[agent] = 2
        self.agent_state = temp

class SIRSimulator:
    def __init__(self, N, I0, beta, mu, t_max):
        self.pop = Population(N, I0)
        self.beta = beta
        self.mu = mu
        self.t_max = t_max
        self.history = []

    def run(self):
        for t in range(self.t_max):
            self.pop.update(self.beta, self.mu)
            self.history.append(np.sum(self.pop.agent_state == 1)/self.pop.N)
        return self.history