import os

import constants as c
import pandas as pd
from config.definitions import ROOT_DIR


def calc_stats_temp(df):

    list_stat_temp_name = ["Gemiddeld",
                           "Minimum",
                           "Maximum",
                           "Dagstand",
                           "Nachtstand",
                           ]

    list_stat_temp = [df['t'].mean(),
                      df['t'].min(),
                      df['t'].max(),
                      c.t_in,
                      c.t_in_nacht,
                      ]

    df_stats_temp = pd.DataFrame({'Naam': list_stat_temp_name,
                                  "Temperatuur [°C]": list_stat_temp})

    return df_stats_temp


def calc_stats_gasboiler(df):

    cost_gas_total = calc_cost_gas(df)

    heat_time = str(str((100 * ((df["w_heatloss"] >= 0).sum() / len(df.index))).round(3)) + "%")

    list_stat_heat_name = ["Gemiddeld warmteverlies",
                           "Minimum warmteverlies",
                           "Maximum warmteverlies",
                           "",
                           "Levering warmte over periode",
                           "Verbruik gas over jaar",
                           "Kosten gas over periode"]

    list_stat_temp = [df['w_heatloss'].mean(),
                      df['w_heatloss'].min(),
                      df['w_heatloss'].max(),
                      "",
                      heat_time,
                      df['p_gas'].sum(),
                      cost_gas_total]

    list_eenheid = ["[W]",
                    "[W]",
                    "[W]",
                    "",
                    "[%]",
                    "[m^3]",
                    "[€]"]

    df_stats_gasboiler = pd.DataFrame({'Naam': list_stat_heat_name,
                                       "Waarden": list_stat_temp,
                                       "Eenheid": list_eenheid})

    return df_stats_gasboiler


def calc_stats_heatpump(df):

    cost_elek_total = calc_cost_elek(df)
    df["SPF"] = df['P_th'].mean() / df['P_el'].mean()
    list_stat_heat_name = ["Gemiddeld warmteverlies",
                           "Minimum warmteverlies",
                           "Maximum warmteverlies",
                           "",
                           "Gemiddeld warmteopbrengst",
                           "Minimum warmteopbrengst",
                           "Maximum warmteopbrengst",
                           "Totaal warmteopbrengst",
                           "",
                           "Gemiddeld elektrische vraag",
                           "Minimum elektrische vraag",
                           "Maximum elektrische vraag",
                           "Totaal elektrisch verbruik",
                           "",
                           "Gemiddeld COP",
                           "Minimum COP",
                           "Maximum COP",
                           "",
                           "SPF",
                           "Kosten elektra over periode"
                           ]

    list_stat_temp = [df['w_heatloss'].mean(),
                      df['w_heatloss'].min(),
                      df['w_heatloss'].max(),
                      "",
                      df['P_th'].mean(),
                      df['P_th'].min(),
                      df['P_th'].max(),
                      df["P_th"].sum(),
                      "",
                      df['P_el'].mean(),
                      df['P_el'].min(),
                      df['P_el'].max(),
                      df["P_el"].sum(),
                      "",
                      df['COP'].mean(),
                      df['COP'].min(),
                      df['COP'].max(),
                      "",
                      df['P_th'].mean() / df['P_el'].mean(),
                      cost_elek_total,
                      ]

    list_eenheid = ["[W]",
                    "[W]",
                    "[W]",
                    "",
                    "[W]",
                    "[W]",
                    "[W]",
                    "[Wh]",
                    "",
                    "[W]",
                    "[W]",
                    "[W]",
                    "[Wh]",
                    "",
                    "[-]",
                    "[-]",
                    "[-]",
                    "",
                    "[-]",
                    "[€]"]

    df_stats_heatpump = pd.DataFrame({'Naam': list_stat_heat_name,
                                      "Waarden": list_stat_temp,
                                      "Eenheid": list_eenheid})

    return df_stats_heatpump


def calc_cost_gas(df):
    price_gas_cons_hour = c.price_gas_cons * 12 / 8765.8
    if df["p_gas"].sum() > 1200:
            x = df["p_gas"].sum() - 1200
            y = len(df.index) * price_gas_cons_hour
            cost_gas_total = 1200 * c.price_gas_var_locked + x * c.price_gas_var_above + y

            return cost_gas_total

    else:
        cost_gas_total = df["p_gas"].sum() * c.price_gas_var_locked + len(df.index) * price_gas_cons_hour

        return cost_gas_total


def calc_cost_elek(df):
    price_elek_cons_hour = c.price_elek_cons * 12 / 8765.8
    if df["P_el"].sum() > 2900000:
            x = (df["P_el"].sum() / 1000) - 2900
            y = len(df.index) * price_elek_cons_hour
            cost_elek_total = 2900 * c.price_elek_var_locked + x * c.price_elek_var_above + y

            return cost_elek_total

    else:
        cost_elek_total = df["P_el"].sum() * c.price_gas_var + len(df.index) * price_elek_cons_hour

        return cost_elek_total

def save_excel(sim_nr, df, df_building):

    save_path = str(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr), 'table') + '/tabel.xlsx')

    df_stats_temp = calc_stats_temp(df)
    df_stats_gasboiler = calc_stats_gasboiler(df)
    df_stats_heatpump = calc_stats_heatpump(df)

    with pd.ExcelWriter(save_path) as writer:
        df_stats_temp.to_excel(writer, sheet_name='Temperatuur')
        df_stats_gasboiler.to_excel(writer, sheet_name='Cv-Ketel')
        df_stats_heatpump.to_excel(writer, sheet_name='Warmtepomp')
        df.to_excel(writer, sheet_name='Data')
        df_building.to_excel(writer, sheet_name='Constructie')