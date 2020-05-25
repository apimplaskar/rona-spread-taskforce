# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:14:33 2020

@author: Aleksandre
"""

import networkx as nx
import numpy as np
import numpy.random as rand
from collections import deque
import matplotlib.pyplot as plt
import math
import scipy.stats as stats

G = nx.gnp_random_graph(1000,0.15)
x = np.linspace (0, 100, 200) 

y1 = stats.gamma.pdf(x, a=4.94, scale=1/.26)
plt.plot(x, y1, "y-", label=(r'$\alpha=29, \beta=3$')) 


plt.ylim([0,.2])
plt.xlim([0,60])
plt.show()

y2 = stats.gamma.pdf(x, a=8.16, scale=1/.33)
plt.plot(x, y2, "y-", label=(r'$\alpha=29, \beta=3$')) 


plt.ylim([0,.2])
plt.xlim([0,60])
plt.show()

y3 = stats.gamma.pdf(x, a=5.81, scale=1/0.95)
plt.plot(x, y3, "y-", label=(r'$\alpha=29, \beta=3$')) 


plt.ylim([0,.2])
plt.xlim([0,60])
plt.show()


def BFS_t(Gr,zero,p,h,d):

        #Prameters:
        #Gr - Graph
        #zero - patient zero
        #p - probability of transmitting infection
            #by a symptomatic host at every itneraction
        #s - probability of developing symptoms once infected
        #h - probability of quarantining once symptomatic
        #r - probability of recovering
        #x - probability of death
        #d - number of days simulation is run


        #Status arrays
        infected = [False] * Gr.number_of_nodes()
        symptomatic = [False] * Gr.number_of_nodes()
        quarantined = [False] * Gr.number_of_nodes()
        recovered = [False] * Gr.number_of_nodes()
        deceased = [False] * Gr.number_of_nodes()
        infected_days = [0] * Gr.number_of_nodes()
        #Metrics
        inf = 1
        rec = 0
        dead = 0
        days_rem = d
        #Result arrays
        queue = []
        infected_nodes = []
        symptomatic_nodes = []
        quarantined_nodes = []
        recovered_nodes = []
        deceased_nodes = []

        # element at position i is the number of infected people on day i
        num_infected_per_day    = []
        num_symptomatic_per_day = []
        num_quarantined_per_day = []
        num_recovered_per_day   = []
        num_deceased_per_day    = []

        queue.append(zero)
        infected[zero] = True
        infected_nodes.append(zero)
        while days_rem > 0:
            days_rem-=1
            
            while queue:
                s = queue.pop(0)
                for i in Gr.neighbors(s):
                    if infected[i] == False and recovered[i] == False and deceased[i] == False and quarantined[i] == False:
                        if rand.uniform(0,10) < p*10:
                            infected[i] = True
                            infected_nodes.append(i)
                            inf+=1
                            
            for i in range(0,len(infected)):
                if quarantined[i] == False:
                    rand_num = rand.uniform(0,10)
                    if symptomatic[i] == False:
                        if rand_num < h*10:
                            quarantined[i] = True
                            quarantined_nodes.append(i)
                    else:
                        if rand_num/2 < h*10:
                            quarantined[i] = True
                            quarantined_nodes.append(i)
                if infected[i] == True:
                    infected_days[i]+=1
                    if symptomatic[i] == False:                           
                            if rand.uniform(0,10) < stats.gamma.pdf(infected_days[i], a=5.81, scale=1/0.95)*10:
                                    symptomatic[i] = True
                                    symptomatic_nodes.append(i)
                            elif rand.uniform(0,10) < stats.gamma.pdf(infected_days[i], a=8.16, scale=1/.33)*10:
                                        recovered[i] = True
                                        rec+=1
                                        recovered_nodes.append(i)
                                        quarantined[i] = False
                                        infected[i] = False
                                        symptomatic[i] = False
                    else:
                            if rand.uniform(0,10) < stats.gamma.pdf(infected_days[i], a=8.16, scale=1/.33)*10:
                                        recovered[i] = True
                                        rec+=1
                                        recovered_nodes.append(i)
                                        quarantined[i] = False
                                        infected[i] = False
                                        symptomatic[i] = False
                            elif rand.uniform(0,10) < stats.gamma.pdf(infected_days[i], a=4.94, scale=1/.26)*10:
                                        deceased[i] = True
                                        dead+=1
                                        deceased_nodes.append(i)
                                        infected[i] = False
                                        symptomatic[i] = False
                                        quarantined[i] = False
                    
                    if quarantined[i] == False and recovered[i] == False and deceased[i] == False:
                        queue.append(i)

            # Update per-day numbers
            num_infected_per_day.append(inf)
            num_symptomatic_per_day.append(len(symptomatic_nodes))
            num_quarantined_per_day.append(len(quarantined_nodes))
            num_recovered_per_day.append(len(recovered_nodes))
            num_deceased_per_day.append(len(deceased_nodes))
            print("day ",(d-days_rem)," infected: ",inf," recovered: ",rec, " deceased: ",dead)        
        return [infected_nodes,quarantined_nodes,symptomatic_nodes,recovered_nodes,deceased_nodes, num_infected_per_day, num_quarantined_per_day, num_symptomatic_per_day, num_recovered_per_day, num_deceased_per_day]

print(BFS_t(G,10,0.3,0.6,28))
