from decision_genetique import DecisionGenetique
from decision_genetique_simplifie import DecisionGenetiqueSimplifie
from simulation import *
import numpy as np
import initial_estimation
from math import inf


def individus_aleatoires(nb_mois, nb_individus):
    return np.array([DecisionGenetiqueSimplifie(nb_mois) for i in range(nb_individus)])

def enfants_permutations_debut_fin(parent1, parent2):
    taille = parent1.nb_mois
    enfant1 = DecisionGenetiqueSimplifie(parent1.nb_mois)
    decisions_enfant1 = list(parent1.decisions[taille//2+1:]) + list(parent2.decisions[:taille//2+1])
    decisions_enfant1 = decisions_enfant1[:taille]
    enfant1.decisions = decisions_enfant1
    enfant2 = DecisionGenetiqueSimplifie(parent1.nb_mois)
    decisions_enfant2 = list(parent2.decisions[taille//2+1:]) + list(parent1.decisions[:taille//2+1])
    decisions_enfant2 = decisions_enfant2[:taille]
    enfant2.decisions = decisions_enfant2
    return [enfant1, enfant2]

def enfant_aleatoire(parent1, parent2):
    taille = parent1.nb_mois
    enfant = DecisionGenetiqueSimplifie(parent1.nb_mois)
    decisions_enfant = []
    index = 0
    while len(decisions_enfant) < taille:
        if (np.random.random() < 0.5):
            parent = parent1
        else:
            parent = parent2
        decisions_enfant.append(parent.decisions[index])
    decisions_enfant = decisions_enfant[:taille]
    enfant.decisions = decisions_enfant
    return enfant

class SolverGenetiqueSimplifie:
    def __init__(self, population_max, taux_conservation, epoch_max=100, duree_simulation=120):
        self.population_max = population_max
        self.epoch = 0
        self.epoch_max = epoch_max
        self.taux_conservation = taux_conservation
        self.generation_en_cours = [DecisionGenetiqueSimplifie(duree_simulation) for i in range(population_max)]
        self.res = []
        self.meilleur_individu = self.generation_en_cours[0]
        self.duree_simulation = duree_simulation # 1 ans

    def selection(self):
        nb_conservation = int(self.taux_conservation * len(self.generation_en_cours))
        ind_meilleurs_res = np.argsort(self.res)
        ind_meilleurs_res = np.flip(ind_meilleurs_res)
        return [fg for fg in np.array(self.generation_en_cours)[ind_meilleurs_res][:nb_conservation]]

    def mutation(self, array):
        nb_enfants = int(1.5 * self.taux_conservation * self.population_max) # 1.5 * 0.2 = 30% d'individus là
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
                pintades = [Pintade(pintade.sexe, 'EXT', 6) for pintade in pintades_initial]
                oeufs = [Oeuf("male", 'EXT') for pintade in pintades_initial]
                oeufs += [Oeuf("femelle", 'EXT') for pintade in pintades_initial]
                actif = Actif(budget_initial, pintades, oeufs)
                sim = Simulation_Simplifie(actif, d.decisions, self.duree_simulation)
                sim.sim()
                treso_finale = sim.actif.treso[-1]
                self.res.append(treso_finale)
                if treso_finale > max_treso:
                    max_treso = treso_finale
                    pourcentages = d.decisions
                    print("pourcentage", pourcentages)
                    print("treso", sim.actif.treso)
                    print("pintades", np.mean([len(pintades) for pintades in sim.actif.pintades]))
                    print("oeufs", np.mean([len(oeufs) for oeufs in sim.actif.oeufs]))
                    self.meilleures_decisions = d
                    d.sauvegarder()
            les_meilleures = self.selection() # 20%
            nb_meilleures = len(les_meilleures)
            mutants = self.mutation(les_meilleures) # 30%
            np.random.shuffle(les_meilleures)
            enfants_permutations = [] # 15%
            for i in range(int(0.75*self.taux_conservation)):
                r_parent_1 = np.random.randint(nb_meilleures)
                r_parent_2 = np.random.randint(nb_meilleures)
                while r_parent_1 == r_parent_2:
                    r_parent_2 = np.random.randint(nb_meilleures)
                parent_1 = les_meilleures[r_parent_1]
                parent_2 = les_meilleures[r_parent_2]
                enfants_permutations.append(enfants_permutations_debut_fin(parent_1, parent_2))
            enfants_aleatoires = [] #15%
            for i in range(int(0.75*self.taux_conservation)):
                r_parent_1 = np.random.randint(nb_meilleures)
                r_parent_2 = np.random.randint(nb_meilleures)
                while r_parent_1 == r_parent_2:
                    r_parent_2 = np.random.randint(nb_meilleures)
                parent_1 = les_meilleures[r_parent_1]
                parent_2 = les_meilleures[r_parent_2]
                enfants_aleatoires.append(enfant_aleatoire(parent_1, parent_2))
            random = individus_aleatoires(self.duree_simulation, self.population_max//5) # 20%
            nouvelles_decisions = np.concatenate([les_meilleures, mutants, enfants_permutations, enfants_aleatoires, random])
            self.generation_en_cours = nouvelles_decisions
            print("---------- epoch ", e + 1, "--- treso init ", budget_initial, "--- max treso ", max_treso)
        return (max_treso, pourcentages, self.meilleures_decisions)


SG = SolverGenetiqueSimplifie(250, 0.2, 200, 12*8)
max_treso, pourcentages, d = SG.resoudre(initial_estimation.budget_initial, initial_estimation.pintadesInit, [])

print(pourcentages)
print(max_treso)

# d = DecisionGenetique(6)
# d.charger("decisions_pintades12-03-2022.ia")
initPintades = [Pintade(pintade.sexe, 'EXT', 6) for pintade in initial_estimation.pintadesInit]
initOeufs = [Oeuf("male", 'EXT') for pintade in initPintades]
initOeufs += [Oeuf("femelle", 'EXT') for pintade in initPintades]

# actif = Actif(initial_estimation.budget_initial, initPintades, initOeufs)
# sim = Simulation_Simplifie(actif, d.decisions, d.nb_mois)

# print(d.decisions)
# sim.sim()
# print("gain ", sim.actif.treso[-1])
# print("oeufs en stock en temps réel avec algo genetique",
#       [len(sim.actif.oeufs[i]) for i in range(len(sim.actif.oeufs))])
# print("pintades en stock en temps réel avec algo genetique",
#       [len(sim.actif.pintades[i]) for i in range(len(sim.actif.pintades))])

# def memePourcentage(initPintades, initOeufs, initialBudget):
#     for i in range (1, 10): 
#         L= [j/i for j in range (8*12)]
#         actif = Actif(initialBudget, initPintades, initOeufs)
#         sim = Simulation_Simplifie(actif, L, len(L))
#         sim.sim()
#         print('--------------- decision', i/10)
#         print("gain ", sim.actif.treso[-1])
#         print("oeufs en stock en temps réel avec algo genetique",
#             [len(sim.actif.oeufs[i]) for i in range(len(sim.actif.oeufs))])
#         print("pintades en stock en temps réel avec algo genetique",
#             [len(sim.actif.pintades[i]) for i in range(len(sim.actif.pintades))])
#     return()

# memePourcentage(initPintades, initOeufs, initial_estimation.budget_initial)


