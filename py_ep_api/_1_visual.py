import _0_util as util, numpy as np, datetime, matplotlib.pyplot as plt
from itertools import cycle

large_font = 20
line_width = 4
lines = ["-","--","-.",":"]
linecycler = cycle(lines)
colors = ['red', 'green', 'blue', 'brown', 'black']
colorcycler = cycle(colors)

result = util.loadJSONFromOutputs('pyep_results')
'''
Warmup days = 15
Starting Simulation at 01/01/2017 for RUNPERIOD 1
Epoch timestamp 1483228800
Timestep 60mins/4 = 15 * 60
'''
drop_warmup = 15 * 24*4
x_date_start = 1483228800
x_date = []
for time_step in range(np.array(result['oat'][drop_warmup:]).shape[0]):
    datetime_time = datetime.datetime.fromtimestamp(x_date_start)
    x_date.append(datetime_time)
    x_date_start = x_date_start + 15*60



fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(x_date,np.array(result['oat'][drop_warmup:]) , color = next(colorcycler), linestyle = next(linecycler),
         label = "Outdoor air temperature [C]",linewidth = line_width)
ax2.plot(x_date, result['elec_hvac'][drop_warmup:],color = next(colorcycler), linestyle = next(linecycler),
         label = "Electricity:HVAC [J]",linewidth = line_width)
# plt.ylabel("Zone Air System Sensible Cooling Rate (W)",fontsize=large_font)
plt.tick_params(axis='both', which='major', labelsize=large_font)

ax1.set_ylabel("Temperature [C]",fontsize=large_font)
ax2.set_ylabel("Electricity [J]",fontsize=large_font)
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2)
plt.show()