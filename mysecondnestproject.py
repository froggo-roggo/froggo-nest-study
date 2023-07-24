import nest
import matplotlib.pyplot as plt

neuron = nest.Create("iaf_psc_alpha")
neuron.set(I_e = 0.0)
multimeter = nest.Create("multimeter")
multimeter.set(record_from = ["V_m"])
spikerecorder = nest.Create("spike_recorder")

noise_ex = nest.Create("poisson_generator") # excitatory spike train
noise_in = nest.Create("poisson_generator") # inhibitory spike train
noise_ex.set(rate=80000.0)
noise_in.set(rate=15000.0)

syn_dict_ex = {"weight": 1.2}
syn_dict_in = {"weight": -2.0}
nest.Connect(noise_ex, neuron, syn_spec=syn_dict_ex)
nest.Connect(noise_in, neuron, syn_spec=syn_dict_in)

nest.Connect(multimeter, neuron)
nest.Connect(neuron, spikerecorder)

nest.Simulate(1000.0)

res = multimeter.get()
Vms = res["events"]["V_m"]
ts = res["events"]["times"]

res2 = spikerecorder.get()
spks = res2["events"]["senders"]
spkts = res2["events"]["times"]


plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(ts, Vms, c = 'r')
plt.title("IF model neuron with two types of input stimuli")
plt.xlim([0,1000])
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Potential (mV)")

plt.subplot(2, 1, 2)
plt.plot(spkts, spks, '|')
plt.xlim([0,1000])
plt.xlabel("Time (ms)")

plt.tight_layout()
plt.show()
plt.savefig('exinsimresult.png')