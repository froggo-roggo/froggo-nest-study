import nest
import matplotlib.pyplot as plt
import numpy
import random



def rancoogen(num, center, ran):
  res = []
  centx, centy = center
  while (num>0):
    xpos = centx + ((random.random())*2 - 1)*ran
    ypos = centy + ((random.random())*2 - 1)*ran
    res.append([xpos, ypos])
    num = num-1
  return res

# distance d and range ran unit: [um]. It will be automatically converted into [mm] in the function.
def randposgen(innerclus, g, d, ran):
  res = []
  if (g<2): return res
  scaled_distance = d/1000;
  scaled_range = ran/1000;
  avdis = scaled_distance * (g-1)
  maxpos = avdis/2
  posnum = numpy.arange(-maxpos, maxpos+scaled_distance, scaled_distance)
  for i in posnum:
    for j in posnum:
      res = res + rancoogen(innerclus, [i, j], scaled_range)
  return res


randpos  = randposgen(5, 5, 200, 30)
pos = nest.spatial.free(pos = randpos)
layer = nest.Create("iaf_psc_alpha", positions = pos)

Vth=-55. # fixed threshold
Vrest=-70. # fixed resting potential
dVms =  {"V_m": [Vrest+(Vth-Vrest)*numpy.random.rand() for x in range(len(layer))]} # randomize initial membrane potential
layer.set(dVms) # set the membrane potential values for each neuron in epop1


mmpos = nest.spatial.grid(shape = [5, 5], extent = [0.2, 0.2])
multimeters = nest.Create("multimeter", positions = mmpos)
multimeters.set({"record_from":["V_m"]})

noise = nest.Create("poisson_generator", 2)
noise[0].rate = 80000.0
noise[1].rate = 15000.0

conn1 = {'rule': 'pairwise_bernoulli',
         'p': nest.spatial_distributions.gaussian(nest.spatial.distance, std=0.2),
         'mask': {'circular': {'radius': 0.75}}
         }
         
conn2 = {'rule': 'pairwise_bernoulli',
         'p': 1.0 - 0.8 * nest.spatial.distance,
         'mask': {'circular': {'radius': 0.75}},
         }

mm_conn_dict = {'rule': 'pairwise_bernoulli', 'p': 0.3}

nest.Connect(noise, layer, syn_spec={"weight": nest.random.uniform(-1.0, 1.0), "delay": 1.0})

'''
plt.figure()
for point in randpos:
  xp, yp = point
  plt.plot(xp, yp, color = 'blue', marker='o')

plt.title("Node distribution")
plt.tight_layout()
plt.show()
plt.savefig('neurons.png')
'''

nest.Connect(layer, layer, conn2)
nest.Connect(multimeters, layer, mm_conn_dict)

nest.Simulate(1000.0)

res = multimeters.get()

recnum = []
tss = []
vmss = []


for i in range(0, 25):
  recnum.append(i)
  tss.append(res["events"][i]["times"])
  vmss.append(res["events"][i]["V_m"])

plt.figure(figsize = (25, 25))
garo = 5
sero = 5
for j in range(0, garo*sero):
    plt.subplot(sero, garo, j+1)
    plt.plot(tss[j], vmss[j], c = 'r', linewidth = "0.1")
    plt.xlim([0,200])
    plt.xlabel("Time (ms)")
    plt.title("multimeter "+str(j+1))
    if(j == round((garo*sero)/2)-1): plt.ylabel("Membrane Potential (mV)")



plt.suptitle('Simulation in a network')
plt.tight_layout()
plt.show()
plt.savefig('nwsm_simple3_200.png')
plt.close()

for j in range(0, garo*sero):
    plt.figure(figsize = (10, 3))
    plt.plot(tss[j], vmss[j], c = 'r', linewidth = "0.1")
    plt.xlim([0,200])
    plt.xlabel("Time (ms)")
    plt.title("multimeter "+str(j+1))
    plt.tight_layout()
    plt.show()
    plt.savefig('simres3/nwsm_simple'+str(j+1)+'_200.png')
    plt.close()