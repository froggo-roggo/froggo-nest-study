import nest
import matplotlib.pyplot as plt
import numpy
import random



def randcoogen(num, center, ran):
  res = []
  if (num == 0): return res
  centx, centy = center
  while (num>0):
    xpos = centx + ((random.random())*2 - 1)*ran
    ypos = centy + ((random.random())*2 - 1)*ran
    res.append([xpos, ypos])
    num = num-1
  return res

# distance d and range ran unit: [um]. It will be automatically converted into [mm] in the function.
def randnodegen(innerclus, g, d, ran):
  res = []
  if (g<2): return res
  scaled_distance = d/1000;
  scaled_range = ran/1000;
  avdis = scaled_distance * (g-1)
  maxpos = avdis/2
  posnum = numpy.arange(-maxpos, maxpos+scaled_distance, scaled_distance)
  for i in posnum:
    for j in posnum:
      if (res == []): res = [randcoogen(innerclus, [i, j], scaled_range)]
      else: res.append(randcoogen(innerclus, [i, j], scaled_range))
    
  return res
  
def whereami(someint, gridsz):
  lft = 0
  rgt = 0
  tp = 0
  bt = 0
  if(someint % gridsz == 0): lft = 1
  if((someint+1) % gridsz == 0): rgt = 1
  if(someint < gridsz): tp = 1
  if(someint >= gridsz*(gridsz-1)): bt = 1
  
  return [lft, rgt, tp, bt]
  

gridsz = 5

randnodepos  = randnodegen(5, gridsz, 200, 30)
nodelist = []
for point in randnodepos:
  pos = nest.spatial.free(pos = point)
  layer = nest.Create("iaf_psc_alpha", positions = pos)
  nodelist.append(layer)


conn1 = {'rule': 'pairwise_bernoulli',
         'p': nest.spatial_distributions.gaussian(nest.spatial.distance, std=0.2),
         'mask': {'circular': {'radius': 0.75}}
         }


conn2 = {'rule': 'pairwise_bernoulli',
         'p': 1.0 - 0.8 * nest.spatial.distance,
         'mask': {'circular': {'radius': 0.75}},
         }


for i in range(0, gridsz*gridsz):
  l, r, t, b = whereami(i)
  if(l&t == 1):
    nest.Connect(node[i], node[i+1], conn1)
    nest.Connect(node[i+1], node[i], conn1)
    nest.Connect(node[i], node[i+1], conn1)
  elif(l&b == 1):
  elif(r&t == 1):
  elif(r&b == 1):
  elif(l == 1):
  elif(r == 1):
  elif(t == 1):
  elif(b == 1):
  else: