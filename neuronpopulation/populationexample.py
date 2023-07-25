import nest
import matplotlib.pyplot as plt
import numpy

pop1 = nest.Create("iaf_psc_alpha", 100)
Vth=-55.0
Vrest=-70.0
dVms =  {"V_m": [Vrest+(Vth-Vrest)*numpy.random.rand() for x in range(len(pop1))]}
pop1.set({"I_e": 376.0})
pop1.set(dVms)
pop2 = nest.Create("iaf_psc_alpha", 100)
multimeters = nest.Create("multimeter", 100)
multimeters.set({"record_from":["V_m"]})

conndict = {"rule": "fixed_indegree", "indegree": 20}
syndict = {"delay": 1.0, "weight":20.0}

nest.Connect(pop1, pop2, conndict, syndict)
nest.Connect(multimeters, pop2, "one_to_one")

nest.Simulate(1000.0)

res = multimeters.get()

sendernum = []
tss = []
vmss = []

for i in range(0, 100):
    sendernum.append(i)
    tss.append(res["events"][i]["times"])
    vmss.append(res["events"][i]["V_m"])
    


garo = 2
sero = 5
for j in range(0, garo*sero):
    plt.subplot(sero, garo, j+1)
    plt.plot(tss[j], vmss[j], c = 'r')
    plt.xlim([0,1000])
    plt.xlabel("Time (ms)")
    if(j == round((garo*sero)/2)-1): plt.ylabel("Membrane Potential (mV)")
    

plt.tight_layout()
plt.show()
plt.savefig('onetoten.png')


plt.figure()
for k in range(0, 100):
    plt.plot(tss[k], vmss[k])
    plt.xlim([0,1000])
    plt.xlabel("Time (ms)")
    #if(j == round((garo*sero)/2)-1): plt.ylabel("Membrane Potential (mV)")
    plt.ylabel("Membrane Potential (mV)")

plt.tight_layout()
plt.show()
plt.savefig('all.png')
