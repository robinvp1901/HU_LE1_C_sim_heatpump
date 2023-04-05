import os

import plotly.graph_objects as go
import constants as c
from config.definitions import ROOT_DIR


def plot_temp(df, sim_nr):

    file_name = str("temperatuur" +
                    "_" + str(c.stationnumber) +
                    "_" + str(c.start_date) +
                    "_" + str(c.end_date))

    # Data stats

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["t"],
        mode='lines',
        line=dict(
              width=0.25,
              color='red',
        ),
        name='Buitentemperatuur [°C]'
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["t_in"],
        mode='lines',
        line=dict(
              width=0.25,
              color='blue',
        ),
        name='Binnentemperatuur [°C]'
    ))

    fig.update_layout(title=dict(font=dict(size=20),
                                 text='Plot temperatuur over periode'),
                      font_family="Arial",
                      xaxis_title='Tijdstempel',
                      yaxis_title='Temperatuur (°C)',
                      width=1200,
                      height=500,
                      plot_bgcolor="#fff",
                      legend=dict(yanchor="top",
                                  y=1,
                                  xanchor="right",
                                  x=1)
                      )

    fig.update_xaxes(gridcolor="#C0C0C0",
                     griddash="dash",
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor="black",
                     minor=dict(ticklen=6, tickcolor="black"))

    fig.update_yaxes(gridcolor="#C0C0C0",
                     griddash="dash",
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor="black",
                     minor_ticks="inside")

    fig.show()
    save_plot(fig, sim_nr, file_name)


def plot_gasboiler(df, sim_nr):

    file_name = str("gasboiler" +
                    "_" + str(c.stationnumber) +
                    "_" + str(c.start_date) +
                    "_" + str(c.end_date))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.index,
                             y=df["P_th_gas"],
                             mode='lines',
                             name='Thermisch vermogen [W]',
                             line=dict(color='red',
                                       width=0.25)
                             )
                  )

    fig.add_trace(go.Scatter(x=df.index,
                             y=df["w_heatloss"],
                             mode='lines',
                             name='Warmteverlies [W]',
                             line=dict(color='blue', width=0.25)
                             )
                  )

    fig.update_layout(title=dict(font=dict(size=20),
                                 text='Plot CV-Ketel'),
                      font_family="Arial",
                      xaxis_title='Tijdstempel',
                      yaxis_title='Vermogen [W]',
                      width=1200,
                      height=500,
                      plot_bgcolor="#fff",
                      legend=dict(yanchor="top",
                                  y=1,
                                  xanchor="right",
                                  x=1)
                      )

    fig.update_xaxes(gridcolor="#C0C0C0",
                     griddash="dash",
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor="black",
                     minor=dict(ticklen=6, tickcolor="black")
                     )

    fig.update_yaxes(gridcolor="#C0C0C0",
                     griddash="dash",
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor="black",
                     minor_ticks="inside"
                     )

    fig.show()

    save_plot(fig, sim_nr, file_name)


def plot_heatpump(df, sim_nr):

    file_name = str("heatpump" +
                    "_" + str(c.stationnumber) +
                    "_" + str(c.start_date) +
                    "_" + str(c.end_date))

    fig = go.Figure()

    # Pth Heatpump
    fig.add_trace(go.Scatter(x=df.index,
                             y=df["P_th"],
                             mode='lines',
                             name='Thermisch vermogen',
                             line=dict(color='red',
                                       width=0.25
                                       )
                             )
                  )

    # Pe Heatpump
    fig.add_trace(go.Scatter(x=df.index,
                             y=df["w_heatloss"],
                             mode='lines',
                             name='Warmteverlies',
                             line=dict(color='blue',
                                       width=0.25
                                       )
                             )
                  )

    fig.add_trace(go.Scatter(x=df.index,
                             y=df["P_el"],
                             mode='lines',
                             name='Elektrisch vermogen',
                             line=dict(color='orange',
                                       width=0.25
                                       )
                             )
                  )

    fig.update_layout(title=dict(font=dict(size=20),
                                 text='Plot Warmtepomp'),
                      font_family="Arial",
                      xaxis_title='Tijdstempel',
                      yaxis_title='Vermogen [W]',
                      width=1200,
                      height=500,
                      plot_bgcolor="#fff",
                      legend=dict(yanchor="top",
                                  y=1,
                                  xanchor="right",
                                  x=1)
                      )

    fig.update_xaxes(gridcolor="#C0C0C0",
                     griddash="dash",
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor="black",
                     minor=dict(ticklen=6, tickcolor="black")
                     )

    fig.update_yaxes(gridcolor="#C0C0C0",
                     griddash="dash",
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor="black",
                     minor_ticks="inside"
                     )

    fig.show()

    save_plot(fig, sim_nr, file_name)


def check_folder(sim_nr):

    if os.path.exists(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr))):
        raise ValueError("Nummer in gebruik")

    if not os.path.exists(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr))):
        os.mkdir(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr)))
        os.mkdir(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr), 'fig'))
        os.mkdir(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr), 'table'))


def save_plot(fig, sim_nr, file_name):

    save_path = str(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr), 'fig', file_name) + '.svg')

    fig.write_image(save_path)
