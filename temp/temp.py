from datetime import time
import pandas as pd

from knmy import knmy
import constants


def load_data_temp(stationnumber, startdate, enddate):
    """
    Met knmy.get hourly wordt doormiddel van het stationnummer, een startdatum en einddatum (YYYYMMDDHH)
    de variable TEMP een temperatuurdataset opgehaald van de gekozen periode.
    Bij het opvragen van de dataset is de tijd en datum gescheiden over 2 kolommen en in een verkeerd
    format. Onderstaande zet deze om naar 1 kolom in YYYY-MM-DD HH
    Namen van kolommen omzetten,
    temperatuur is gegeven met 1 decimaal, zonder scheidingsteken
    Kolommen met data verwijderen, welke niet nodig zijn.
    """
    df = knmy.get_hourly_data(stations=[stationnumber],
                              start=startdate,
                              end=enddate,
                              variables=['TEMP'],
                              parse=True)[3:]
    df = pd.DataFrame(df[0])

    df["YYYYMMDD"] = pd.to_datetime(df["YYYYMMDD"], format='%Y%m%d')
    df["YYYYMMDD"] += pd.to_timedelta(df["H"], unit='h')
    df.rename(columns={'YYYYMMDD': 'tijdstempel', "T": "t"}, inplace=True)
    df["t"] = df["t"] * 0.1
    df.drop(columns=['STN', 'H', 'TD', 'T10N'], inplace=True, axis=1)
    df.set_index("tijdstempel", inplace=True)

    return df


def set_temp(df, start_time, end_time):
    """
    Set de gebruikers temperatuur voor binnen in over de periode. Hierbij kan er gekozen worden voor constant
    op dezelfde temperatuur of nachtschakeling.
    """
    df['t_in'] = constants.t_in_nacht
    mask = df.between_time(time(start_time), time(end_time - 1))
    df.loc[mask.index, 't_in'] = constants.t_in

    df['t_adj'] = df['t_in']
    df['t_average'] = df['t'].mean()

    df['t_out_corr'] = df['t'] + (0.016
                                  * constants.tauw
                                  * 0.8)
    df['t_corr1'] = constants.t_corr1
    df['t_corr2'] = constants.t_corr2

    return df
