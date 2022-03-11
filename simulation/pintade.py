from numpy import random
from oeuf import Oeuf
from const import prix_vente_adulte_inte, prix_vente_adulte_exte, prix_vente_vielle_exte, prix_vente_vielle_inte

class Pintade:
    def __init__(self, sexe, env):
        self.age = 0 # mois
        self.sexe = sexe
        self.env = env

    def pondre(self):
        if (self.age > 6) and (self.sexe == "femelle"): # 6 mois
            rSex = random.random()
            if (rSex > 0.5):
                sexe = "femelle"
            else:
                sexe = "male"
            return Oeuf(sexe, self.env)
        return None

    def vendre(self):
        if (self.age == 0):
            return 0
        if (self.age >= 6): # adulte
            if (self.env == "EXT"):
                return prix_vente_adulte_exte
            else:
                return prix_vente_adulte_inte
        else: # vielle
            if (self.env == "EXT"):
                return prix_vente_vielle_exte
            else:
                return prix_vente_vielle_inte