import itertools
import numpy as np
import initial_estimation
from simulation import Actif, Simulation
from time import time


class Solver:
    def __init__(self, max_etape):
        self.nombre_max_etape = max_etape  # nombre de mois

    def resoudre(self):
        x = np.linspace(0.95, 0, 20)
        pourcentages_chaque_mois = itertools.product(x, repeat=4)
        max = 0
        arg_max = -1
        sim_max = None
        for p in pourcentages_chaque_mois:
            actif = Actif(initial_estimation.budget_initial, initial_estimation.pintadesInit, [])
            simulation = Simulation(actif, p, self.nombre_max_etape)
            treso_totale = simulation.sim()
            treso_finale = treso_totale[-1]
            if treso_finale > max:
                sim_max = simulation
                max = treso_finale
                arg_max = p
                print('treso initiale : ', treso_totale[0])
                print('treso max : ', max)
                print('pourcentages : ', arg_max)
                print("oeufs chaque mois",
                      [len(simulation.actif.oeufs[i]) for i in range(len(simulation.actif.oeufs))])
                print("pintades en stock en temps réel",
                      [len(simulation.actif.pintades[i]) for i in range(len(simulation.actif.pintades))])
                print('------------------- ')
        return arg_max, sim_max


t1 = time()
solver = Solver(120)
arg_max, sim_max = solver.resoudre()
t2 = time()
print('meilleur pourcentage : ', arg_max)
print("evolution mensuelle treso : ", sim_max.actif.treso)
print("qte oeufs mensuelle : ",
      [len(sim_max.actif.oeufs[i]) for i in range(len(sim_max.actif.oeufs))])
print("qte pintades mensuelle : ",
      [len(sim_max.actif.pintades[i]) for i in range(len(sim_max.actif.pintades))])
print('temps total : ', t2 - t1)
