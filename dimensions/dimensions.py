import math


def calc_volume(df_building, name):
    """
    Bereken de inhoud van de woning, eerst worden alle waarden uit de dataset
    omgezet in een lijst en daarna met elkaar vermendigvuldigd.
    """

    volume_dim = []
    df_building_outside = df_building.query("df_s == 'bu'")
    df_building_outside = df_building_outside.droplevel(0)

    for i, j in zip(name[0], name[1]):
        volume_dim.append(df_building_outside.loc[i][j])

    volume = math.prod(volume_dim)

    return volume


def calc_surface(df_building, name):
    """
    Bereken de buiten oppervlaktes, eerst worden alle waarden uit de dataset omgezet in
    een lijst, onderverdeeld in gevelzij, voorgevel, achtergevel, vloerdeel 1e verdieping.
    """
    surf_dim = []
    df_building_outside = df_building.query("df_s == 'bu'")
    df_building_outside = df_building_outside.droplevel(0)

    for i, j in zip(name[0], name[1]):
        surf_dim.append(df_building_outside.loc[i][j])

    surf_gz = math.prod(surf_dim[:2]) + math.prod(surf_dim[2:4])
    surf_vg = math.prod(surf_dim[4:6]) + math.prod(surf_dim[6:8])
    surf_ag = math.prod(surf_dim[8:10]) + math.prod(surf_dim[10:12])
    surf_vl = math.prod(surf_dim[12:14])

    a_surf = surf_gz + surf_vg + surf_ag + surf_vl

    return a_surf


def calc_bhulp(df_building):
    """
    Bereken oppervlakte woning uit om tot hulpwaarden te komen.
    Nodig woonbaar opp, totale oppervlak en lengte buitenkant woning
    """
    df_building_outside = df_building.query("df_s == 'bu'")
    df_building_outside = df_building_outside.droplevel(0)

    df_building_ground = df_building.query("df_s == 'bg'")
    df_building_ground = df_building_ground.droplevel(0)

    df_building_adjacent_above_below = df_building.query("df_s == 'ab'")
    df_building_adjacent_above_below = df_building_adjacent_above_below.droplevel(0)

    a_living = (df_building_ground.loc['Vloer-KR-BG']['Eff Opp. [m]']
                + df_building_adjacent_above_below.loc['Vloer-SS-02']['Eff Opp. [m]'])

    a_tot = a_living * 0.55

    outside_length = (df_building_outside.loc['Muur-GZ-01-01']["Lengte [m]"]
                      + df_building_outside.loc['Muur-VG-01-02']["Lengte [m]"]
                      + df_building_outside.loc['Muur-AG-01-03']["Lengte [m]"])

    b_hulp = 2 * a_living / outside_length

    if b_hulp <= 2:
        b_hulp = 2
        return b_hulp, a_tot

    elif b_hulp >= 50:
        b_hulp = 50
        return b_hulp, a_tot

    else:
        return b_hulp, a_tot
