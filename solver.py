import itertools
import numpy as np

class Solver:
    def __init__(self, max_etape):
        self.ensemble_simulation = None
        self.ensemble_decisions = None
        self.max = 0
        self.argmax = []
        self.nombre_max_etape = max_etape  # nombre de mois

    def resoudre(self):
        x = np.linspace(4000, 0, 10).astype(int)
        mois = itertools.product(x, repeat=4)
        decisions = []
        max = 0
        argMax = -1
        for p in itertools.product(mois, repeat=self.nombre_max_etape):
            #sim
            print(p)



solver = Solver(10)
solver.resoudre()