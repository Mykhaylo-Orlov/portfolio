# projects/seir_model/seir_simulator.py
import numpy as np

class SEIRSimulator:
    def __init__(self, N=500, I0=0.01, beta=0.3, sigma=0.2, mu=0.1, t_max=200):
        self.N = N
        self.I0 = I0
        self.beta = beta
        self.sigma = sigma
        self.mu = mu
        self.t_max = t_max
        self.history = []

    def initialize(self):
        # 0=S, 1=E, 2=I, 3=R
        self.state = np.zeros(self.N, dtype=int)
        infected_idx = np.random.choice(self.N, size=int(self.I0*self.N), replace=False)
        self.state[infected_idx] = 2  # start as infected

    def step(self):
        new_state = self.state.copy()
        for i, s in enumerate(self.state):
            if s == 0:  # Susceptible
                # contact random agent
                contact = np.random.randint(0, self.N)
                if self.state[contact] == 2 and np.random.rand() < self.beta:
                    new_state[i] = 1  # move to exposed
            elif s == 1:  # Exposed
                if np.random.rand() < self.sigma:
                    new_state[i] = 2  # move to infected
            elif s == 2:  # Infected
                if np.random.rand() < self.mu:
                    new_state[i] = 3  # move to recovered
        self.state = new_state

    def run(self):
        self.initialize()
        for t in range(self.t_max):
            self.step()
            # store counts
            counts = np.array([(self.state == i).sum() for i in range(4)])
            self.history.append(counts / self.N)
        return np.array(self.history)