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

edict = {"I_e": 200.0, "tau_m": 20.0} # Parameter default value dictionary setting
nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha") # "exc_iaf_psc_alpha" is a new customized model forked from iaf_psc_alpha, a predefined, built-in model in NEST.
nest.SetDefaults("exc_iaf_psc_alpha", edict) # And then set default values for the customized model

epop1 = nest.Create("exc_iaf_psc_alpha", 100)
epop2 = nest.Create("exc_iaf_psc_alpha", 100)
ipop1 = nest.Create("inh_iaf_psc_alpha", 30)
ipop2 = nest.Create("inh_iaf_psc_alpha", 30)

parameter_dict = {"I_e": [200.0, 150.0], "tau_m": 20.0, "V_m": [-77.0, -66.0]}
pop3 = nest.Create("iaf_psc_alpha", 2, params=parameter_dict)

print("=========== pop3 parameters ===========")
print(pop3.get(["I_e", "tau_m", "V_m"])) # able to check customized parameters of all neurons in the population
print("=======================================")

Vth=-55. # fixed threshold
Vrest=-70. # fixed resting potential
dVms =  {"V_m": [Vrest+(Vth-Vrest)*numpy.random.rand() for x in range(len(epop1))]} # randomize initial membrane potential
epop1.set(dVms) # set the membrane potential values for each neuron in epop1
# the former two lines are equivalent to: epop1.set({"V_m": Vrest + nest.random.uniform(0.0, Vth-Vrest)})


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
# note that the population number n of epops and ipops are different
# therefore the number of all possible connection between the nodes is 100 * 30 = 3000
nest.Connect(ipop1, epop1, conn_dict_in, syn_dict_in)