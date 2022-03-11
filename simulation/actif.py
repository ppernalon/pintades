class Actif:
    def __init__(self, treso0, pintades0, oeufs0):
        self.treso = [treso0]
        self.pintades = [pintades0]
        self.oeufs = [oeufs0]
        self.etape = 0

    def vendre_pintades(self, adulte_femelle_int, adulte_femelle_exte):
        
        for pintade in self.pintades[self.etape]:
            pintade.vendre()