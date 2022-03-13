from datetime import date

import numpy as np


class DecisionGenetiqueSimplifie:
    def __init__(self, nb_mois):
        self.nb_mois = nb_mois
        self.decisions = np.random.rand(nb_mois, 1)

    def sauvegarder(self):
        with open('decisions_pintades' + date.today().strftime("%d-%m-%Y") + '.ia', 'w') as f:
            for ligne in self.decisions:
                for element in ligne:
                    f.write(str(element))
                    f.write('\n')

    def charger(self, fichier):
        with open(fichier, 'r') as f:
            lines = f.read().splitlines()
            donnees = [float(line) for line in lines]
            decisions = []
            d = 0
            for i in range(self.nb_mois + 1):
                #mois = []
                #for k in range(4):
                 #   d += 1
                 #   mois.append(donnees[d])
                decisions.append(donnees[i])
            print(decisions)
            self.decisions = decisions

    def mutation(self):
        def array_mutation(array, taux_mutation):
            nouveau_array = []
            for ligne in array:
                nouvelle_ligne = []
                for element in ligne:
                    nouveau_element = element
                    if (np.random.random() < 0.75):
                        element += (np.random.random() - 0.5) * taux_mutation * element
                    nouvelle_ligne.append(nouveau_element)
                nouveau_array.append(nouvelle_ligne)
            return np.array(nouveau_array)

        max_mutation = 0.15
        nouvelles_decisions = DecisionGenetiqueSimplifie(self.nb_mois)
        nouvelles_decisions.decisions = array_mutation(self.decisions, max_mutation)

        return nouvelles_decisions
