
from temp import temp
from simulation import simulation as sim
from simulation import plot, stats
from dimensions import dimensions as dim

import constants as c
"""
Om een dataset van de buitentemperatuur te maken,
kies een begin en einddatum (incl. uur) bij het
dichtbijzijnde KNMI weerstation van de betreffende woning.
"""


def run(sim_nr):
    df = temp.load_data_temp(stationnumber=c.stationnumber,
                             startdate=c.start_date,
                             enddate=c.end_date)
    df = temp.set_temp(df,
                       start_time=c.time_start,
                       end_time=c.time_end)


    df_building = sim.load_data_building()

    volume = dim.calc_volume(df_building, name=c.names_volume_dim)
    a_surf = dim.calc_surface(df_building, name=c.names_surf_dim)
    b_hulp, a_tot = dim.calc_bhulp(df_building)

    c_eff, qi, qv = sim.calc_variables_ventilation(volume,
                                                   a_surf,
                                                   a_tot,
                                                   x=c.sp_ceff,
                                                   y=c.qis
                                                   )

    df = sim.calc_fiak(df)
    # df = sim.calc_fiak2(df)
    df = sim.calc_figk(df)

    df = sim.calc_heatloss_outside(df_building, df)
    df = sim.calc_heatloss_adjacent(df_building, df)
    df = sim.calc_heatloss_ground(df_building, df, b_hulp,
                                  dv=c.dv,
                                  fgw=c.fgw
                                  )
    df = sim.calc_heatloss_ventilation(df, qi, qv,
                                       cp=c.cp,
                                       z=c.z,
                                       fv=c.fv
                                       )
    df = sim.calc_heatloss_sp(df)
    df = sim.calc_heatloss(df)

    df = sim.gas_boiler(df)
    df = sim.calc_heatpump(df)

    plot.check_folder(sim_nr)
    plot.plot_temp(df, sim_nr)
    plot.plot_gasboiler(df, sim_nr)
    plot.plot_heatpump(df, sim_nr)
    stats.save_excel(sim_nr, df, df_building)


if __name__ == '__main__':
    sim_nr = input("Give number : ")
    run(sim_nr)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
