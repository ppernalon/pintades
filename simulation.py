import numpy as np

from math import inf
from const import prix_oeuf_inte, prix_oeufs_exte, prix_vente_adulte_inte, prix_vente_adulte_exte, \
    prix_vente_vielle_exte, prix_vente_vielle_inte, nombre_maximal_pintades, cout_nouriture, cout_oeuf, cout_veto, \
    cout_pintade_inte, cout_pintade_exte
from numpy import random, where


class Oeuf:
    def __init__(self, sexe, env):
        self.sexe = sexe
        self.env = env

    def eclore(self):
        return Pintade(self.sexe, self.env)

    def vendre(self):
        if self.env == "EXT":
            return prix_oeufs_exte
        else:
            return prix_oeuf_inte


class Pintade:
    def __init__(self, sexe, env, age=0):
        self.age = age  # mois
        self.sexe = sexe
        self.env = env

    def vieillir(self):
        self.age += 1

    def pondre(self):
        if (self.age > 6) and (self.sexe == "femelle"):  # 6 mois
            r_sexe = random.random()
            if r_sexe > 0.5:
                sexe = "femelle"
            else:
                sexe = "male"
            return Oeuf(sexe, self.env)
        return None

    def vendre(self):
        if self.age == 0:
            return 0
        if self.age >= 6:  # adulte
            if self.env == "EXT":
                return prix_vente_adulte_exte
            else:
                return prix_vente_adulte_inte
        else:  # vielle
            if self.env == "EXT":
                return prix_vente_vielle_exte
            else:
                return prix_vente_vielle_inte


class Actif:
    def __init__(self, treso0, pintades0, oeufs0):
        self.treso = [treso0]
        self.pintades = [pintades0]
        self.oeufs = [oeufs0]
        self.etape = 0

    def initialiser_etape(self):
        self.etape += 1
        self.treso.append(self.treso[self.etape - 1])
        self.oeufs.append(list(self.oeufs[self.etape - 1]))
        self.pintades.append(list(self.pintades[self.etape - 1]))
        for pintade in self.pintades[self.etape]:
            pintade.vieillir()

    def oeufs_ext(self):
        oeufs = self.oeufs[self.etape]
        oeufs_ext = []
        for oeuf in oeufs:
            if oeuf.env == "EXT":
                oeufs_ext.append(oeuf)
        return oeufs_ext

    def oeufs_int(self):
        oeufs = self.oeufs[self.etape]
        oeufs_int = []
        for oeuf in oeufs:
            if oeuf.env == "INT":
                oeufs_int.append(oeuf)
        return oeufs_int

    def femelle_ext(self):
        pintades = self.pintades[self.etape]
        pintades_ext = []
        for pintade in pintades:
            if pintade.env == "EXT" and pintade.sexe == "femelle" and 6*12 > pintade.age >= 6:
                pintades_ext.append(pintade)
        return pintades_ext

    def femelle_int(self):
        pintades = self.pintades[self.etape]
        pintades_int = []
        for pintade in pintades:
            if pintade.env == "INT" and pintade.sexe == "femelle" and 6*12 > pintade.age >= 6:
                pintades_int.append(pintade)
        return pintades_int

    def poussins(self):
        pintades = self.pintades[self.etape]
        poussins = []
        for pintade in pintades:
            if pintade.age < 6:
                poussins.append(pintade)
        return poussins

    def vendre_pintades(self, adulte_femelle_int, adulte_femelle_ext):
        sorted_by_ages = list(self.pintades[self.etape])
        sorted_by_ages.sort(key=(lambda p: p.age), reverse=True)
        nb_vendu_int = 0
        nb_vendu_ext = 0
        index = 0
        count = len(sorted_by_ages)
        pintade_a_enlever = []
        while index < count:
            pintade_a_vendre = sorted_by_ages[index]
            vendu = False
            if pintade_a_vendre.sexe == "male":
                vendu = True
            if pintade_a_vendre.age > 6 * 12:  # 6 ans
                vendu = True
            if (pintade_a_vendre.sexe == "femelle") and (pintade_a_vendre.env == "EXT") and (
                    nb_vendu_ext < adulte_femelle_ext) and (pintade_a_vendre.age > 6):
                nb_vendu_ext += 1
                vendu = True
            if (pintade_a_vendre.sexe == "femelle") and (pintade_a_vendre.env == "INT") and (
                    nb_vendu_int < adulte_femelle_int) and (pintade_a_vendre.age > 6):
                nb_vendu_int += 1
                vendu = True
            if vendu:
                self.treso[self.etape] += pintade_a_vendre.vendre()
                pintade_a_enlever.append(pintade_a_vendre)
            index += 1
        for pintade in pintade_a_enlever:
            sorted_by_ages.remove(pintade)
        self.pintades[self.etape] = sorted_by_ages

    def vendre_oeufs(self, oeuf_int, oeuf_ext):
        nb_vendu_int = 0
        nb_vendu_ext = 0
        oeufs = list(self.oeufs[self.etape])
        nb_oeufs = len(oeufs)
        oeuf_a_jeter = []
        for index in range(nb_oeufs):
            oeuf = oeufs[index]
            vendu = False
            if (oeuf.env == "EXT") and nb_vendu_ext < oeuf_ext:
                nb_vendu_ext += 1
                vendu = True
            if (oeuf.env == "INT") and nb_vendu_int < oeuf_int:
                nb_vendu_int += 1
                vendu = True
            if vendu:
                self.treso[self.etape] += oeuf.vendre()
                oeuf_a_jeter.append(oeuf)
        for oeuf in oeuf_a_jeter:
            oeufs.remove(oeuf)
        self.oeufs[self.etape] = oeufs

    def passer_etaper(self):
        self.etape += 1


class Simulation:
    def __init__(self, actif, decisions, max_etape):
        self.actif = actif
        self.etape = 0
        self.etape_final = max_etape
        self.decisions = decisions

    def respect_des_contraintes(self):
        treso_positive = self.actif.treso[self.etape] >= 0
        nombre_pintades = 0 < len(self.actif.pintades[self.etape]) < nombre_maximal_pintades

        return treso_positive and nombre_pintades

    def calculer_etape(self):
        decision_en_cours = self.decisions

        self.actif.initialiser_etape()
        self.etape += 1

        # vente
        nb_femelle_ext = int(decision_en_cours[0] * len(self.actif.femelle_ext()))
        nb_femelle_int = int(decision_en_cours[1] * len(self.actif.femelle_int()))
        nb_oeuf_ext = int(decision_en_cours[2] * len(self.actif.oeufs_ext()))
        nb_oeuf_int = int(decision_en_cours[3] * len(self.actif.oeufs_int()))
        self.actif.vendre_oeufs(nb_oeuf_int, nb_oeuf_ext)
        self.actif.vendre_pintades(nb_femelle_int, nb_femelle_ext)

        # eclosion
        nouvelles_pintades = []
        oeuf_a_enlever = []
        for oeuf in self.actif.oeufs[self.etape]:
            pintade = oeuf.eclore()
            nouvelles_pintades.append(pintade)
            self.actif.treso[self.etape] -= cout_veto
            oeuf_a_enlever.append(oeuf)
        for oeuf in oeuf_a_enlever:
            self.actif.oeufs[self.etape].remove(oeuf)

        # ponte
        nouveaux_oeufs = []
        for pintade in self.actif.pintades[self.etape]:
            for k in range(30 // 3):
                oeuf = pintade.pondre()
                if oeuf is not None:
                    nouveaux_oeufs.append(oeuf)

        # mise a jour des attributs
        self.actif.pintades[self.etape] += nouvelles_pintades
        self.actif.oeufs[self.etape] += nouveaux_oeufs

        # cout pour l'étape
        nb_poussins = len(self.actif.poussins())
        nb_total_pintades = len(self.actif.pintades[self.etape])
        self.actif.treso[self.etape] -= ( nb_total_pintades - nb_poussins / 2) * cout_nouriture / 12  # nourriture
        for pintadeDebutEtape in self.actif.pintades[self.etape]:
            if pintadeDebutEtape.env == "EXT":
                self.actif.treso[self.etape] -= cout_pintade_inte
            else:
                self.actif.treso[self.etape] -= cout_pintade_exte

    def sim(self):
        for i in range(self.etape_final):
            if not (self.respect_des_contraintes()):
                return self.actif.treso + [-1]
            self.calculer_etape()
        return self.actif.treso



class Simulation_Genetique:
    def __init__(self, actif, decisions, max_etape):
        self.actif = actif
        self.etape = 0
        self.etape_final = max_etape
        self.decisions = decisions

    def respect_des_contraintes(self):
        treso_positive = self.actif.treso[self.etape] >= 0
        nombre_pintades = 0 < len(self.actif.pintades[self.etape]) < nombre_maximal_pintades

        return treso_positive and nombre_pintades

    def calculer_etape(self):

        self.actif.initialiser_etape()
        self.etape += 1
        nb_femelle_ext = len(self.actif.femelle_ext())
        nb_femelle_int = len(self.actif.femelle_int())
        nb_oeuf_ext = len(self.actif.oeufs_int())
        nb_oeuf_int = len(self.actif.oeufs_ext())
        decision_etape = self.decisions[self.etape]

        # vente
        nb_femelle_ext_vendre = int(decision_etape[0] * nb_femelle_ext)
        nb_femelle_int_vendre = int(decision_etape[1] * nb_femelle_int)
        nb_oeuf_ext_vendre = int(decision_etape[2] * nb_oeuf_ext)
        nb_oeuf_int_vendre = int(decision_etape[3] * nb_oeuf_int)
        self.actif.vendre_oeufs(nb_oeuf_int_vendre, nb_oeuf_ext_vendre)
        self.actif.vendre_pintades(nb_femelle_int_vendre, nb_femelle_ext_vendre)

        # eclosion
        nouvelles_pintades = []
        oeuf_a_enlever = []
        for oeuf in self.actif.oeufs[self.etape]:
            pintade = oeuf.eclore()
            nouvelles_pintades.append(pintade)
            self.actif.treso[self.etape] -= cout_veto
            oeuf_a_enlever.append(oeuf)
        for oeuf in oeuf_a_enlever:
            self.actif.oeufs[self.etape].remove(oeuf)

        # ponte
        nouveaux_oeufs = []
        for pintade in self.actif.pintades[self.etape]:
            for k in range(30 // 3):
                oeuf = pintade.pondre()
                if oeuf is not None:
                    nouveaux_oeufs.append(oeuf)

        # mise a jour des attributs
        self.actif.pintades[self.etape] += nouvelles_pintades
        self.actif.oeufs[self.etape] += nouveaux_oeufs

        # cout pour l'étape
        nb_poussins = len(self.actif.poussins())
        nb_total_pintades = len(self.actif.pintades[self.etape])
        self.actif.treso[self.etape] -= ( nb_total_pintades - nb_poussins / 2) * cout_nouriture / 12  # nourriture
        for pintadeDebutEtape in self.actif.pintades[self.etape]:
            if pintadeDebutEtape.env == "EXT":
                self.actif.treso[self.etape] -= cout_pintade_inte
            else:
                self.actif.treso[self.etape] -= cout_pintade_exte

    def sim(self):
        for i in range(self.etape_final):
            self.calculer_etape()
            if not (self.respect_des_contraintes()):
                self.actif.treso[-1] = -inf
                return self.actif.treso
        return self.actif.treso
