from fonction_genetique import FonctionGenetique
from simulation import *
import numpy as np
import initial_estimation
from math import inf


def fonctions_aleatoires(nb):
    return np.array([FonctionGenetique(5, 4) for i in range(nb)])


class SolverGenetique:
    def __init__(self, nb_fg, taux_conservation, epoch_max=100):
        self.nb_fonction_genetique = nb_fg
        self.epoch = 0
        self.epoch_max = epoch_max
        self.taux_conservation = taux_conservation
        self.fonctions_genetiques = [FonctionGenetique(5, 4) for i in range(nb_fg)]
        self.res = [0 for i in range(nb_fg)]
        self.meilleure_fonction_genetique = self.fonctions_genetiques[0]
        self.duree_simulation = 12  # 1 ans

    def selection(self):
        nb_conservation = int(self.taux_conservation * len(self.fonctions_genetiques))
        ind_meilleurs_res = np.argsort(self.res)
        ind_meilleurs_res = np.flip(ind_meilleurs_res)
        return [fg for fg in np.array(self.fonctions_genetiques)[ind_meilleurs_res][:nb_conservation]]

    def mutation(self, array):
        nb_enfants = int(
            self.nb_fonction_genetique * (1 - self.taux_conservation - 0.3))  # 20% de nouvelles fg aleatoires
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
            fonctions_genetiques = [fg for fg in self.fonctions_genetiques]
            for fg in fonctions_genetiques:
                pintades = [Pintade(pintade.sexe, pintade.env, pintade.age) for pintade in pintades_initial]
                oeufs = [oeuf for oeuf in oeufs_initial]
                actif = Actif(budget_initial, pintades, oeufs)
                sim = Simulation_Genetique(actif, fg, self.duree_simulation)
                sim.sim()
                treso_finale = sim.actif.treso[-1]
                self.res.append(treso_finale)
                if treso_finale > max_treso:
                    max_treso = treso_finale
                    pourcentages = sim.decisions
                    self.meilleure_fonction_genetique = fg
                    fg.sauvegarder()
            les_meilleures = self.selection()
            enfants = self.mutation(les_meilleures)
            fonctions_alea = fonctions_aleatoires(self.nb_fonction_genetique - len(les_meilleures) - len(enfants))
            nouvelles_fonctions = np.concatenate([les_meilleures, enfants, fonctions_alea])
            self.fonctions_genetiques = nouvelles_fonctions
            print("---------- epoch ", e + 1, "--- treso init ", budget_initial, "--- max treso ", max_treso)
        return (max_treso, pourcentages, self.meilleure_fonction_genetique)


SG = SolverGenetique(100, 0.2, 100)
max_treso, pourcentages, meilleures_fonctions = \
    SG.resoudre(initial_estimation.budget_initial, initial_estimation.pintadesInit, [])

print(max_treso)