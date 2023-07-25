import nest
import matplotlib.pyplot as plt
import numpy

'''
ndict = {"I_e": 200.0, "tau_m": 20.0}
nest.SetDefaults("iaf_psc_alpha", ndict)
neuronpop1 = nest.Create("iaf_psc_alpha", 100)
neuronpop2 = nest.Create("iaf_psc_alpha", 100)
neuronpop3 = nest.Create("iaf_psc_alpha", 100)
'''
### 1. Creation setting
noise = nest.Create("poisson_generator", 2)
noise[0].rate = 80000.0
noise[1].rate = 15000.0

edict = {"I_e": 500.0} # Parameter default value dictionary setting
nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha") # "exc_iaf_psc_alpha" is a new customized model forked from iaf_psc_alpha, a predefined, built-in model in NEST.
nest.SetDefaults("exc_iaf_psc_alpha", edict) # And then set default values for the customized model

idict = {"I_e": 1000.0} # Parameter default value dictionary setting
nest.CopyModel("iaf_psc_alpha", "inh_iaf_psc_alpha", params=idict) # Fork and set default in one line

epop1 = nest.Create("exc_iaf_psc_alpha", 100)
epop2 = nest.Create("exc_iaf_psc_alpha", 100)
ipop1 = nest.Create("inh_iaf_psc_alpha", 30)
ipop2 = nest.Create("inh_iaf_psc_alpha", 30)



Vth=-55. # fixed threshold
Vrest=-70. # fixed resting potential
dVms =  {"V_m": [Vrest+(Vth-Vrest)*numpy.random.rand() for x in range(len(epop1))]} # randomize initial membrane potential
epop1.set(dVms) # set the membrane potential values for each neuron in epop1
epop2.set({"V_m": Vrest + nest.random.uniform(0.0, Vth-Vrest)})
ipop1.set({"V_m": Vrest + nest.random.uniform(0.0, Vth-Vrest)})
ipop2.set({"V_m": Vrest + nest.random.uniform(0.0, Vth-Vrest)})


### 2. Connection setting

d = 1.0
Je = 2.0
Ke = 20
Ji = -4.0
Ki = 12
conn_dict_ex = {"rule": "fixed_indegree", "indegree": Ke}
conn_dict_in = {"rule": "fixed_indegree", "indegree": Ki}
syn_dict_ex = {"delay": d, "weight": Je}
syn_dict_in = {"delay": d, "weight": Ji}
nest.Connect(epop1, ipop1, conn_dict_ex, syn_dict_ex)
nest.Connect(epop1, epop2, conn_dict_ex, syn_dict_ex)
nest.Connect(ipop2, epop2, conn_dict_in, syn_dict_in)
nest.Connect(ipop1, epop2, conn_dict_in, syn_dict_in)

nest.Connect(noise, epop2, syn_spec={"weight": nest.random.uniform(-1.0, 1.0), "delay": 1.0})

### 3. Device setting
#pg = nest.Create("poisson_generator")
#pg.set({"start": 100.0, "stop": 150.0})

#recdict = {"record_to" : "ascii", "label" : "epop2_mp"}

multinum = 50

mm1 = nest.Create("multimeter", multinum) #params=recdict)
mm1.set({"record_from":["V_m"]})

mm_conn_dict = {'rule': 'pairwise_bernoulli', 'p': 0.3}
nest.Connect(mm1, epop2, mm_conn_dict)

nest.Simulate(1000.0)

res = mm1.get()

sendernum = []
tss = []
vmss = []

for i in range(0, multinum):
    sendernum.append(i)
    tss.append(res["events"][i]["times"])
    vmss.append(res["events"][i]["V_m"])



plt.figure(figsize = (14, 20))

garo = 2
sero = 5
for j in range(0, garo*sero):
    plt.subplot(sero, garo, j+1)
    plt.plot(tss[j], vmss[j], c = 'r', linewidth = "0.1")
    plt.xlim([0,1000])
    plt.xlabel("Time (ms)")
    plt.title("Epop 2 node "+str(j+1))
    if(j == round((garo*sero)/2)-1): plt.ylabel("Membrane Potential (mV)")
    
plt.suptitle('Simulation with poisson noise')
plt.tight_layout()
plt.show()
plt.savefig('onetoten_epop_4.png')


    
plt.figure(figsize = (10, 5))
for k in range(0, multinum):
    plt.plot(tss[k], vmss[k], linewidth = "0.01")
    plt.xlim([0,1000])
    plt.xlabel("Time (ms)")
    #if(j == round((garo*sero)/2)-1): plt.ylabel("Membrane Potential (mV)")
    plt.ylabel("Membrane Potential (mV)")

plt.suptitle('Simulation with poisson noise')
plt.tight_layout()
plt.show()
plt.savefig('all_epop_4.png')
