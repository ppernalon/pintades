import matplotlib.pyplot as plt
from simulation import *
import initial_estimation
from decision_genetique_simplifie import DecisionGenetiqueSimplifie

initPintades = [Pintade(pintade.sexe, 'EXT', 6) for pintade in initial_estimation.pintadesInit]
initOeufs = [Oeuf("male", 'EXT') for pintade in initPintades]
initOeufs += [Oeuf("femelle", 'EXT') for pintade in initPintades]
d = DecisionGenetiqueSimplifie(8*12)
d.charger("decisions_pintades13-03-2022.ia")

actif = Actif(initial_estimation.budget_initial, initPintades, initOeufs)
sim = Simulation_Simplifie(actif, d.decisions, d.nb_mois)

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