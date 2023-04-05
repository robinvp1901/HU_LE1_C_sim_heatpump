# Constants simulation
# =================

# Parameter prijzen
price_gas_cons = 19.44        # Vaste aansluitkosten gas per maand TODO Vaste maand bedrag verwerken in calc.
price_gas_var = 2.71        # Prijs per m3
price_elek_cons = 24.49       # Vaste aansluitkosten elektra per maand TODO Vaste maand bedrag verwerken in calc.
price_elek_var = 0.79       # Prijs per KwH

price_gas_var_locked = 1.45         # Prijs per m3
price_gas_var_above = 3.66          # Prijs per m3

price_elek_var_locked = 0.40        # Prijs per KwH
price_elek_var_above = 0.83         # Prijs per KwH


# Parameter periode
stationnumber = 260
start_date = 2021010101
end_date = 2021123124
# Parameter tijd
time_hour = 3600

# Parameter CV-Ketel
eff_boiler = 95
sp_combustion = 35.17 * 10**6

# Parameter Warmtepomp



#     Parameters temperatuur
"""Constante waarde voor ontwerpbinnentemperatuur, ontwerpbuitentemperatuur,
correctie temperatuur delta1/2 en jaarlijkse gemiddelde"""

t_in = 19               # Ontwerpbinnentemperatuur  [°C]
t_in_nacht = 16         # Ontwerpbinnentemperatuur in nachtstand  [°C]
t_out = -9              # Ontwerpbuitentemperatuur  [°C]
t_corr1 = 3             # Correctie temperatuur delta1 [°C]
t_corr2 = -1            # Correctie temperatuur delta2 [°C]
# t_average = 9           # Jaarlijks gemiddelde [°C]

# Tijd normaalstand TODO Support voor minuten en seconde inbouwen
time_start = 9          # Starttijd normaalstand HH, mm , ss
time_end = 22           # eindtijd normaalstnad HH, mm , ss

# Parameters warmtecapaciteit woning
sp_ceff = 50            # Specifieke capaciteit [Wh/(m³·K)]
tauw = 50               # Startwaarde tauw TODO Loop voor tauw maken

"""Constante waarde voor aangrenzende woning"""
# Parameters aangrenzende woning
# t_adj = 15              # Temperatuur aangrenzende woning [°C]
cz = 1                  # Zekeheids klasse [-]

"""Constante waarde voor luchtverversing woning"""
# Parameters luchtverversing
t_corr_air = 0          # Correctie luchttemperatuur [°C]
cp = 1200               # Soortelijk warmte [J/(m³·K)]
z = 0.5                 # Fractie infiltratie [-]
qis = 0.0019            # Luchtstroom infiltratie [m³/s per m²]
fv = 1                  # Correctiefactor inblaastemperaturen [-]

"""Constante waarde voor constructie woning"""
#     Parameters constructie woning
dv = 0                  # Diepte onder maaiveld [m]
fgw = 1                 #


"""
Onderstaande zijn lijsten gemaakt waarop het calculatie programma van de dimensies de juiste waarde uit de 
database van de woning kan halen om berekeningen uit te voeren
"""
# Gegevens van beide verdiepingen woning voor inhoud
names_volume_dim = [
    ('Muur-GZ-BG-01', 'Muur-VG-BG-02', 'Muur-GZ-BG-01', 'Muur-GZ-01-01', 'Muur-VG-01-02', 'Muur-GZ-01-01'),
    ("Lengte [m]", "Lengte [m]", "Breedte [m]", "Lengte [m]", "Lengte [m]", "Breedte [m]")]

# first 3 dim BG, second 3 dim 1e floor

# Gegevens om buiten oppervlak woning te kunnen bepalen
names_surf_dim = [
    ('Muur-GZ-BG-01', 'Muur-GZ-BG-01', 'Muur-GZ-01-01', 'Muur-GZ-01-01',
     'Muur-VG-BG-02', 'Muur-VG-BG-02', 'Muur-VG-01-02', 'Muur-VG-01-02',
     'Muur-AG-BG-03', 'Muur-AG-BG-03', 'Muur-AG-01-03', 'Muur-AG-01-03',
     "Vloer-VD-01", "Vloer-VD-01"),
    ("Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
     "Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
     "Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
     "Lengte [m]", "Breedte [m]", "Lengte [m]", "Breedte [m]",
     "Lengte [m]", "Breedte [m]")]

name_living_BG = [('Vloer-KR-BG', 'Vloer-KR-BG'), ("Lengte [m]", "Breedte [m]")]
name_living_1e = [('Vloer-SS-02', 'Vloer-SS-02'), ("Lengte [m]", "Breedte [m]")]
