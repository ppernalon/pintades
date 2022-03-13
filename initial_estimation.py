from simulation import Pintade
import const


def suite(u_0, N):
    u_n = [u_0]
    budgetByDay = 0
    for k in range(1, N + 1):
        if const.nombre_maximal_pintades > u_n[-1]:  # On borne le nombre de Pintades
            if k <= 182 or (k > 182 and k % 3 != 0):
                u_n.append(u_n[-1])
            if k > 182 and k % 3 == 0:
                if (u_n[-1] + (u_n[k - 1 - 182]) // 2 < const.nombre_maximal_pintades):
                    u_n.append(u_n[-1] + (u_n[k - 1 - 182]) // 2)
                else:
                    u_n.append(u_n[-1])
            if 728 < k <= 1092:
                budgetByDay += 0.079 * u_n[k]
        else:
            u_n.append(u_n[-1])
            budgetByDay += 0.079 * u_n[k]
    return u_n[-1], u_n[727], budgetByDay


nber_pintades_initial = suite(2, 728)[0]


def budget(suite):
    suite = suite(2, 1092)
    twoYearNber = suite[1]
    threeYearNber = suite[0]
    budgetEstimation = 3.5 * (threeYearNber - twoYearNber) + suite[2]
    return (budgetEstimation)


budget_initial = (budget(suite) / 12) * 3


def initialisation_pintades(N):
    u_n = [2]
    pintades = [Pintade("femelle", "EXT", 24), Pintade("femelle", "INT", 24)]
    for k in range(1, N + 1):
        if k <= 182 or (k > 182 and k % 3 != 0):
            u_n.append(u_n[-1])
        if k > 182 and k % 3 == 0:
            age = (2 * 365 - k) // 30
            u_n.append(u_n[-1] + (u_n[k - 1 - 182]) // 2)
            for i in range((u_n[k - 1 - 182]) // 4):
                pintades.append(Pintade("femelle", "EXT", 6))
                pintades.append(Pintade("femelle", "INT", 6))
    return (u_n[-1], pintades)


pintadesInit = initialisation_pintades(450)[1]