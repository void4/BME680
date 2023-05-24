import json
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import ScalarFormatter
from dateutil import parser
from collections import defaultdict
import numpy as np


keys = "pressure_hpa humidity temperature_celsius gas_kohms".split()# 
colors = "blue green red black".split()

values = {}

fig, ax = plt.subplots(layout="constrained", num="BME680 sensor measurements")

offset = 60

for k, key in enumerate(keys):
	if k == 0:
		axes = {key:ax}
		ax.set_ylabel(key)
		ax.yaxis.label.set_color(colors[0])
		xy, = ax.plot([], [], color=colors[k], label=key)
		lines = {key:xy}
	else:
		axes[key] = ax.twinx()
		
		lines[key] = axes[key].plot([], [], color=colors[k], label=key)[0]
		
		axes[key].set_ylabel(key)
		axes[key].yaxis.label.set_color(colors[k])
		
		if k > 1:
			axes[key].spines["right"].set_position(("outward", offset*(k-1)))

	values[key] = []

fig.legend()

def update(frame):

	with open("measurements.jsonl") as f:
		flines = f.read().splitlines()

	values = defaultdict(list)

	for line in flines:
		try:
			ts, js = line.split(" ", 1)
			timestamp = parser.parse(ts)
			j = json.loads(js)
		except ValueError as e:
			#print(e)
			continue
		
		#print(j)
	
		
		if not all([key in j for key in keys]):
			continue
		
		values["xs"].append(timestamp)#j["start"])
		#print(j)
		
		for key in keys:
			values[key].append(j[key])
		
	for key in keys:
		
		lines[key].set_data(values["xs"], values[key])		
	
		ax = axes[key]
		ax.relim()
		ax.autoscale_view()
		#plt.yticks(np.arange(960,1030,10))
		ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))
		ax.xaxis.set_major_locator(AutoDateLocator())

		#ax.yaxis.set_major_formatter(ScalarFormatter())
		ax.ticklabel_format(axis="y", useOffset=False)
#ax.yaxis.set_major_locator(AutoDateLocator())

	return list(lines.values()),

animation = FuncAnimation(fig, update, interval=200)
#plt.ticklabel_format(axis='y', style='plain')
plt.show()
