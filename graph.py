import matplotlib.pyplot as plt
from simulation import *
import initial_estimation
from decision_genetique_simplifie import DecisionGenetiqueSimplifie

initPintades = [Pintade(pintade.sexe, 'EXT', 6) for pintade in initial_estimation.pintadesInit]
initOeufs = [Oeuf("male", 'EXT') for pintade in initPintades]
initOeufs += [Oeuf("femelle", 'EXT') for pintade in initPintades]
d = DecisionGenetiqueSimplifie(8*12)
d.charger("decisions_pintades13-03-2022.ia")

d = """0.0 0.04 0.6 0.52 0.62 0.23 0.98 0.02 0.31 0.38 0.59 0.08 0.24 0.1
 0.24 0.83 0.93 0.08 0.0 0.02 0.24 0.55 0.27 0.79 0.98 0.1 0.32 0.06
 0.13 0.58 0.73 0.06 0.57 0.18 0.55 0.02 0.32 0.53 0.23 0.48 0.5 0.18
 0.88 0.56 0.41 0.27 0.06 0.35 0.4 0.36 0.25 0.26 0.47 0.18 0.04 0.66
 0.56 0.37 0.02 0.1 0.07 0.42 0.16 0.89 0.96 0.26 0.08 0.04 0.28 0.72
 0.0 0.8 0.47 0.36 0.64 0.0 0.35 0.31 0.14 0.92 0.19 0.76 0.36 0.04
 0.04 0.45 0.52 0.54 0.24 1.0 0.0 0.64 0.62 0.61 0.55 0.89"""

d = d.split(" ")
d = [float(v) for v in d]
a = DecisionGenetiqueSimplifie(8*12)
a.decisions = d
a.sauvegarder()

actif = Actif(initial_estimation.budget_initial, initPintades, initOeufs)
sim = Simulation_Simplifie(actif, d, len(d))

# print(d.decisions)
sim.sim()
print("gain ", sim.actif.treso)
print("oeufs en stock en temps réel avec algo genetique",
      [len(sim.actif.oeufs[i]) for i in range(len(sim.actif.oeufs))])
print("pintades en stock en temps réel avec algo genetique",
      [len(sim.actif.pintades[i]) for i in range(len(sim.actif.pintades))])

mois = [i for i in range(12*8 + 1)]
nb_oeufs = [len(sim.actif.oeufs[i]) for i in range(len(sim.actif.oeufs))]
nb_pintades = [len(sim.actif.pintades[i]) for i in range(len(sim.actif.pintades))]

# oeuf
plt.plot(mois, nb_oeufs)
plt.ylabel("Nombre d'oeufs")
plt.xlabel("Mois")
plt.show()

# pintades
plt.plot(mois, nb_pintades)
plt.ylabel("Nombre de pintades")
plt.xlabel("Mois")
plt.show()

# treso
plt.plot(mois, sim.actif.treso)
plt.ylabel("Trésorerie")
plt.xlabel("Mois")
plt.show()