from datetime import date

import numpy as np
import const


class FonctionGenetique:
    def __init__(self, nb_entrees, nb_sorties):
        self.nb_entrees = nb_entrees
        self.nb_sorties = nb_sorties
        self.nb_neurones = 1000
        self.matrix1 = np.random.rand(nb_entrees, self.nb_neurones)
        self.matrix2 = np.random.rand(self.nb_neurones, nb_sorties)

    def evaluate(self, X):
        def activation1(L):
            n = len(L)
            for i in range(n):
                if L[i] < 0:
                    L[i] = 0

        def activation2(L):
            n = len(L)
            for i in range(n):
                temp = np.tanh(L[i])
                L[i] = temp

        X = X / const.nombre_maximal_pintades
        output1 = np.dot(X.T[0], self.matrix1)
        activation1(output1)
        output2 = np.dot(output1, self.matrix2)
        activation2(output2)

        return output2

    def sauvegarder(self):
        genome1, genome2 = self.matrix1, self.matrix2
        with open('fg_pintades' + date.today().strftime("%d-%m-%Y") + '.ia', 'w') as f:
            for i in range(len(genome1)):
                for j in range(len(genome1[0])):
                    f.write("%s\n" % genome1[i][j])
            for i in range(len(genome2)):
                for j in range(len(genome2[0])):
                    f.write("%s\n" % genome2[i][j])

    def charger(self, fichier):
        with open(fichier, 'r') as f:
            lines = f.read().splitlines()
            donnees = [float(line) for line in lines]
            genome1 = [[0 for i in range(self.nb_neurones)] for j in range(self.nb_entrees)]
            genome2 = [[0 for i in range(self.nb_sorties)] for j in range(self.nb_neurones)]
            k = 0
            for i in range(self.nb_entrees):
                for j in range(self.nb_neurones):
                    genome1[i][j] = donnees[k]
                    k += 1
            for i in range(self.nb_neurones):
                for j in range(self.nb_sorties):
                    genome2[i][j] = donnees[k]
                    k += 1
            self.matrix1 = genome1
            self.matrix2 = genome2

    def mutation(self):
        def array_mutation(array, taux_mutation):
            nouveau_array = []
            for ligne in array:
                nouvelle_ligne = []
                for element in ligne:
                    nouveau_element = element
                    if (np.random.random() < 0.20):
                        element += (np.random.random() - 0.5) * taux_mutation * element
                    nouvelle_ligne.append(nouveau_element)
                nouveau_array.append(nouvelle_ligne)
            return np.array(nouveau_array)

        max_mutation = 0.15
        nouvelle_fg = FonctionGenetique(self.nb_entrees, self.nb_sorties)
        nouvelle_fg.matrix1 = array_mutation(self.matrix1, max_mutation)
        nouvelle_fg.matrix2 = array_mutation(self.matrix2, max_mutation)
        return nouvelle_fg
