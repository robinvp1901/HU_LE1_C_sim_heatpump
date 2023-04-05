import os
from config.definitions import ROOT_DIR
sim_nr = "001"


print(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr)))
if not os.path.exists(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr))):
    os.mkdir(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr)))
    os.mkdir(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr), 'fig'))
    os.mkdir(os.path.join(ROOT_DIR, "output", ('sim_' + sim_nr), 'table'))
