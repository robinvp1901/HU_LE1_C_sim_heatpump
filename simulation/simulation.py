from hplib import hplib as hpl
import pandas as pd

import constants as c

CSV_file = "database/data.csv"
type_buitenmuur = "Buitenmuur"
type_muur_aangrenzend = "Binnenmuur"
type_muur_aangrenzend_boven_onder = "Bovenburen"
type_vloer_bg = "Vloer-BG"


def load_data_building():
    """
    Bouwgegevens van woning wordt uit een csv lijst gehaald, gesorteerd op type en samengevoegd
    in de dataframe met een multi-index.
    """
    df_building = pd.read_csv(CSV_file,
                              sep=',',
                              skiprows=2).set_index("Naam")

    df_bu = df_building[df_building["Type"] == type_buitenmuur]
    df_aa = df_building[df_building["Type"] == type_muur_aangrenzend]
    df_ab = df_building[df_building["Type"] == type_muur_aangrenzend_boven_onder]
    df_bg = df_building[df_building["Type"] == type_vloer_bg]

    list_df = [df_bu,
               df_aa,
               df_ab,
               df_bg]
    df_building = pd.concat(list_df,
                            keys=['bu', 'aa', 'ab', 'bg'],
                            names=['df_s'])

    return df_building

# TODO Variabelen bundel in series
def calc_variables_ventilation(volume, a_surf, a_tot, x, y):
    """
    Importeer gegevens vanuit dimensies en constantes om de variable voor
    de ventilatie woning uit te rekenen.
    """
    c_eff = volume * x                     # Calc opslagcapaciteit [Wh/K]
    qi = y * a_surf                        # Calc volumestroom infiltration [m³/s]
    qv = 0.0009 * a_tot                    # Calc volumestroom ventilation [m³/s]

    return c_eff, qi, qv


def calc_fiak(df):
    """
    Importeer gegevens vanuit constantes en dataset temperatuur om de
    variablen voor de aanliggende woning uit te rekenen.
    """
    # correctiefactor fiak voor wanden
    df['fiak'] = ((df['t_in'] - df['t_adj'])
                  / (df['t_in'] - df['t_out_corr'])
                  )

    # correctiefactor fiak voor plafond naar bovengelegen woning
    df['fiak2'] = (((df['t_in'] + df['t_corr1']) - df['t_adj'])
                   / (df['t_in'] - df['t_out_corr'])
                   )

    return df


def calc_figk(df):
    """
    Importeer gegevens vanuit constantes en dataset temperatuur om de
    variabele temperatuur voor de grond uit te rekenen.
    """
    # correctiefactor figk voor grond
    df['figk'] = ((df["t_in"] + df['t_corr2'])
                  - df['t_average']) / (df['t_in'] - df["t_out_corr"])

    return df


def calc_heatloss_outside(df_building, df):
    """
    Importeer bouwgegevens uit dataframe om warmteverlies
    via de buitenmuren te berekenen.
    """
    df_building_outside = df_building.query("df_s == 'bu'")


    df['h_out'] = (df_building_outside["Eff Opp. [m]"]
                   * df_building_outside["fk"]
                   * (df_building_outside["U-Waarde contructie"]
                      + df_building_outside["U-Waarde Thermische bruggen"])
                   ).sum()

    return df

# TODO h_adjacent_above_below mist, met fiak2 vermenigvuldigen
def calc_heatloss_adjacent(df_building, df):
    """
    Importeer bouwgegevens uit dataframe en calc_fiak om warmteverlies
    via de aangrenzende woning uit te rekenen.
    """
    df_building_adjacent = df_building.query("df_s == ['aa', 'ab']")
    df_building_adjacent = df_building_adjacent.droplevel(0)

    df['h_adj'] = (df_building_adjacent["Eff Opp. [m]"]
                   * (df_building_adjacent["U-Waarde contructie"]
                      + df_building_adjacent["U-Waarde Thermische bruggen"])
                   ).sum()

    df['h_adj'] = df['h_adj'] * df['fiak']

    return df


def calc_heatloss_ground(df_building, df, b_hulp, dv, fgw):
    """
    Importeer bouwgegevens uit dataframe, calc_figk en constants om warmteverlies
    via de grond uit te rekenen.
    """
    df_building_ground = df_building.query("df_s == 'bg'")

    df['h_gr'] = (df_building_ground["Eff Opp. [m]"]
                  * (0.9671 / (-7.455
                               + (10.76 + b_hulp) ** 0.5532
                               + (9.773 + dv) ** 0.6027
                               + (0.0265 + df_building_ground["U-Waarde contructie"]
                                  + df_building_ground["U-Waarde Thermische bruggen"])
                               ** -0.9226)
                     + -0.0203)
                  * fgw
                  ).sum() * 1.45

    df['h_gr'] = df['h_gr'] * df['figk']

    return df


def calc_heatloss_ventilation(df, qi, qv, cp, z, fv):
    """
    Importeer gegevens vanuit constantes em calc_variables_ventilation
    om het warmteverlies van de ventilatie te berekenen.
    """
    h_infiltration = cp * qi * z
    h_filtration = cp * qv * fv

    df['h_ven'] = h_infiltration + h_filtration

    return df


def calc_heatloss_sp(df):
    """
    Specifieke warmteverlies van verschillende componenten met elkaar
    optellen tot een totaal.
    """
    df['h_tot'] = df['h_out'] + df['h_adj'] + df['h_gr'] + df['h_ven']  # TODO h_adj toevoegen

    return df


def calc_heatloss(df):
    """
    Specifieke warmteverlies vermendigvuldigen met temperatuurverschil
    binnen en buiten om de warmteverlies op het tijdstip te berekenen.
    """

    df['w_heatloss'] = df['h_tot'] * (df['t_in'] - df['t_out_corr'])

    return df


def gas_boiler(df):
    """
    1. Neem de vraag op vanuit datatabel
    2. Bereken hoeveel aardgas verbrandt is
    3. Als de waarde lager is dan 0, set waarde op 0
    """

    df["P_th_gas"] = (df["w_heatloss"] / (c.eff_boiler / 100))
    df["p_gas"] = 3600 * df["P_th_gas"] / c.sp_combustion
    df['p_gas'].mask(df['p_gas'] <= 0, 0, inplace=True)

    return df


def calc_heatpump(df):
    """
    1. Haal eerst de parameters op van de gekozen warmtepomp.
    2. Bereken de prestatie van de warmtepomp per datapunt doormiddel van de parameters: buitentemperatuur, systeemtemperatuur, gevraagd warmte.
    3. Als de uitkomsten negatief zijn, maskeer dit dan met 0.
    """
    database = hpl.load_database()


    # Load parameters
    parameters = hpl.get_parameters(model='WSAN-YMi 91')

    # WH - SDC0305J3E5 / WH - UD03JE5

    # Create heat pump object with parameters
    heatpump = hpl.HeatPump(parameters)
    df["T_out"] = 32 - 5 #TODO zet dit in vaste parameters
    # Whereas mode = 1 is for heating and mode = 2 is for cooling
    results = heatpump.simulate(t_in_primary=df['t_out_corr'].values,
                                t_in_secondary=df['T_out'].values,
                                t_amb=df['t_out_corr'].values,
                                p_th_min=df["w_heatloss"],
                                mode=1)

    results = pd.DataFrame.from_dict(results).set_index(df.index)
    df = pd.concat([df, results], axis=1)
    df['COP'].mask(df['w_heatloss'] <= 0, 0, inplace=True)
    df['P_el'].mask(df['w_heatloss'] <= 0, 0, inplace=True)
    df['P_th'].mask(df['w_heatloss'] <= 0, 0, inplace=True)
    df['m_dot'].mask(df['w_heatloss'] <= 0, 0, inplace=True)

    return df
