class Solver:
    def __init__(self, max_etape):
        self.ensemble_simulation = None
        self.ensemble_decisions = None
        self.max = 0
        self.argmax = []
        self.nombre_max_etape = max_etape  # nombre de mois

    def generer_decisions(self):
        a = 2
