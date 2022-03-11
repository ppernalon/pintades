from const import prix_oeuf_inte, prix_oeufs_exte
from pintade import Pintade

class Oeuf:
    def __init__(self, sexe, env):
        self.sexe = sexe
        self.env = env
    
    def eclore(self):
        return Pintade(self.sexe, self.env)

    def vendre(self):
        if self.env == "EXT":
            return prix_oeufs_exte
        else :
            return prix_oeuf_inte