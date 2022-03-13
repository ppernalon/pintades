from decision_genetique import DecisionGenetique
from simulation import *
import numpy as np
import initial_estimation
from math import inf


def individus_aleatoires(nb_mois, nb_individus):
    return np.array([DecisionGenetique(nb_mois) for i in range(nb_individus)])


class SolverGenetique:
    def __init__(self, population_max, taux_conservation, epoch_max=100, duree_simulation=120):
        self.population_max = population_max
        self.epoch = 0
        self.epoch_max = epoch_max
        self.taux_conservation = taux_conservation
        self.generation_en_cours = [DecisionGenetique(duree_simulation) for i in range(population_max)]
        self.res = []
        self.meilleur_individu = self.generation_en_cours[0]
        self.duree_simulation = duree_simulation # 1 ans

    def selection(self):
        nb_conservation = int(self.taux_conservation * len(self.generation_en_cours))
        ind_meilleurs_res = np.argsort(self.res)
        ind_meilleurs_res = np.flip(ind_meilleurs_res)
        return [fg for fg in np.array(self.generation_en_cours)[ind_meilleurs_res][:nb_conservation]]

    def mutation(self, array):
        # 20% de nouveaux individus aleatoires
        nb_enfants = int(self.population_max * (1 - self.taux_conservation - 0.3))
        nb_enfants_produits = 0
        enfants = []
        while nb_enfants_produits < nb_enfants:
            for fg in array:
                enfants.append(fg.mutation())
                nb_enfants_produits = len(enfants)
                if (nb_enfants_produits > nb_enfants):
                    break
        return np.array(enfants)

    def resoudre(self, budget_initial, pintades_initial, oeufs_initial):
        max_treso = -inf
        pourcentages = []
        for e in range(self.epoch_max):
            self.res = []
            generation = [individu for individu in self.generation_en_cours]
            for d in generation:
                pintades = [Pintade(pintade.sexe, pintade.env, pintade.age) for pintade in pintades_initial]
                oeufs = [oeuf for oeuf in oeufs_initial]
                actif = Actif(budget_initial, pintades, oeufs)
                sim = Simulation_Genetique(actif, d.decisions, self.duree_simulation)
                sim.sim()
                treso_finale = sim.actif.treso[-1]
                self.res.append(treso_finale)
                if treso_finale > max_treso:
                    max_treso = treso_finale
                    pourcentages = d.decisions
                    self.meilleures_decisions = d
                    d.sauvegarder()
            les_meilleures = self.selection()
            enfants = self.mutation(les_meilleures)
            fonctions_alea = individus_aleatoires(self.duree_simulation, self.population_max - len(les_meilleures) - len(enfants))
            nouvelles_fonctions = np.concatenate([les_meilleures, enfants, fonctions_alea])
            self.generation_en_cours = nouvelles_fonctions
            print("---------- epoch ", e + 1, "--- treso init ", budget_initial, "--- max treso ", max_treso)
            # print(pourcentages)
        return (max_treso, pourcentages, self.meilleures_decisions)


SG = SolverGenetique(400, 0.2, 100, 6)
max_treso, pourcentages, d = SG.resoudre(initial_estimation.budget_initial, initial_estimation.pintadesInit, [])

# print(pourcentages)
# print(max_treso)

# d = DecisionGenetique(6)
# d.charger("decisions_pintades12-03-2022.ia")
actif = Actif(initial_estimation.budget_initial, initial_estimation.pintadesInit, [])
sim = Simulation_Genetique(actif, d.decisions, d.nb_mois)
sim.sim()
print("gain ", sim.actif.treso[-1])
print("oeufs en stock en temps réel avec algo genetique",
      [len(sim.actif.oeufs[i]) for i in range(len(sim.actif.oeufs))])
print("pintades en stock en temps réel avec algo genetique",
      [len(sim.actif.pintades[i]) for i in range(len(sim.actif.pintades))])
