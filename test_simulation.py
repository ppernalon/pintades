from simulation import *


def jeteste():
    pintades_ext = [Pintade("male", "EXT", i) for i in range(12)] + [Pintade("femelle", "EXT", i) for i in range(12)]
    pintades_int = [Pintade("male", "INT", i) for i in range(12)] + [Pintade("femelle", "INT", i) for i in range(12)]
    pintades = pintades_ext + pintades_int

    oeufs_ext = [Oeuf("Male", "EXT") for i in range(4)] + [Oeuf("femelle", "EXT") for i in range(4)]
    oeufs_int = [Oeuf("Male", "INT") for i in range(4)] + [Oeuf("femelle", "INT") for i in range(4)]
    oeufs = oeufs_int + oeufs_ext

    actif = Actif(20000, pintades, oeufs)

    decisions = [[0, 0, 200, 200] for i in range(12 * 7)]
    # nb_femelle_ext, nb_femelle_int, nb_oeuf_ext,nb_oeuf_int

    simulation = Simulation(actif, decisions)
    print(simulation.sim())
    print("oeufs en stock en temps réel", [len(simulation.actif.oeufs[i]) for i in range(len(simulation.actif.oeufs))])
    print("pintades en stock en temps réel", [len(simulation.actif.pintades[i]) for i in range(len(simulation.actif.pintades))])


jeteste()
