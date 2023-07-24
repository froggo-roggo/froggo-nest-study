import nest
import matplotlib.pyplot as plt

neuron1 = nest.Create("iaf_psc_alpha")
neuron1.set({"I_e": 300.0})
neuron2 = nest.Create("iaf_psc_alpha")
neuron2.set({"I_e": 400.0})

multimeter = nest.Create("multimeter")
multimeter.set(record_from = ["V_m"])

spikerecorder1 = nest.Create("spike_recorder")
spikerecorder2 = nest.Create("spike_recorder")

nest.Connect(multimeter, neuron1)
nest.Connect(multimeter, neuron2)
nest.Connect(neuron1, spikerecorder1)
nest.Connect(neuron2, spikerecorder2)

nest.Simulate(500.0)

dmm = multimeter.get()
Vms1 = dmm["events"]["V_m"][0:-1:2]
Vms2 = dmm["events"]["V_m"][1:-1:2]
ts1 = dmm["events"]["times"][0:-1:2]
ts2 = dmm["events"]["times"][1:-1:2]

plt.figure(1)
plt.plot(ts1, Vms1, c = 'r')
plt.plot(ts2, Vms2, c = 'b')
plt.title("IF model neuron")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Potential (mV)")

import os
curfilename = os.path.basename(__file__)
plt.legend(["neuron 1 (300.0 pA)", "neuron 2 (400.0 pA)"], bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.tight_layout()
plt.show()
plt.savefig(curfilename+'.png')
