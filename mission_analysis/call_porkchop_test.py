from mission_analysis.Porkchop import Porkchop

import time
import pykep as pk

StartTime = time.time()

# 0. Inputs

# direct transfer from Planet_i to Planet_f
Planet_i = pk.planet.jpl_lp('earth')
Planet_f = pk.planet.jpl_lp('mars')

# input epoch range
Epoch_i = 9600
Epoch_f = 10000

# input Time of flights to be considered
# note: ToF_min minimum value = 1
ToF_min = 1
ToF_max = 600

# Show the pork?
ShowPork = True

# 1. create porkchop data from inputs
porkchop = Porkchop(Planet_i, Planet_f, Epoch_i, Epoch_f, ToF_min, ToF_max, ShowPork)

# 2. data generation
data = porkchop.get_data()

# 3. Report on porkchop data

EndTime = time.time()

porkchop.report(data)
print(f"{'Run time (sec): '}\t{EndTime - StartTime}")

# 3. Produce porkchop plot
porkchop.get_plot(data[0], data[1], data[2], data[6])