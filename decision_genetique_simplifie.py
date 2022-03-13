from datetime import date

import numpy as np


class DecisionGenetiqueSimplifie:
    def __init__(self, nb_mois):
        self.nb_mois = nb_mois
        self.decisions = np.random.randint(100, size=nb_mois)/100

    def sauvegarder(self):
        with open('decisions_pintades' + date.today().strftime("%d-%m-%Y") + '.ia', 'w') as f:
            for element in self.decisions:
                f.write(str(element))
                f.write('\n')                    

    def charger(self, fichier):
        with open(fichier, 'r') as f:
            lines = f.read().splitlines()
            donnees = [float(line) for line in lines]
            decisions = []
            d = 0
            for i in range(self.nb_mois):
                #mois = []
                #for k in range(4):
                 #   d += 1
                 #   mois.append(donnees[d])
                decisions.append(donnees[i])
            self.decisions = decisions

    def mutation(self):
        def array_mutation(array, taux_mutation):
            nouveau_array = []
            for element in array:
                nouveau_element = element
                if (np.random.random() < 0.66):
                    r_signe = np.random.random()
                    if (r_signe > 0.5):
                        nouveau_element += taux_mutation
                    else:
                        nouveau_element -= taux_mutation
                if (nouveau_element > 1): nouveau_element = 1
                if (nouveau_element < 0): nouveau_element = 0
                nouveau_array.append(nouveau_element)
            return np.array(nouveau_array)

        taux_mutation = 0.02
        nouvelles_decisions = DecisionGenetiqueSimplifie(self.nb_mois)
        nouvelles_decisions.decisions = array_mutation(self.decisions, taux_mutation)

        return nouvelles_decisions
