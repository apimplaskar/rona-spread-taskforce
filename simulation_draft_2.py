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


G = nx.gnp_random_graph(300,0.15)




def BFS_t(Gr,zero,p,s,h,r,x,d):

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
        
        if d%2 == 0:
            nrows = int(d/2)
        else:
            nrows = int(d/2)+1
        ncols = 2
        f, axes = plt.subplots(nrows, ncols, figsize = (40,40))

        # Plotting variables
        days = [i for i in range(1,d+1)]
        numInfected = []
        #Status arrays
        infected = [False] * Gr.number_of_nodes()
        symptomatic = [False] * Gr.number_of_nodes()
        quarantined = [False] * Gr.number_of_nodes()
        recovered = [False] * Gr.number_of_nodes()
        deceased = [False] * Gr.number_of_nodes()
        infected_days = [0] * Gr.number_of_nodes()
        symptomatic_days = [0] * Gr.number_of_nodes()
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

        queue.append(zero)
        infected[zero] = True
        infected_nodes.append(zero)
        while days_rem > 0:
            days_rem-=1
            print("day ",(d-days_rem)," infected at start ",inf," recovered ",rec, " deceased ",dead)
            while queue:
                s = queue.pop(0)
                for i in Gr.neighbors(s):
                    if infected[i]==False and recovered[i] == False:
                            if rand.uniform(0,10) < p*10:
                                infected[i] = True
                                infected_nodes.append(i)
                                inf+=1

            for i in range(0,len(infected)):
                if infected[i] == True:
                    infected_days[i]+=1
                    if symptomatic[i] == False:
                            if rand.uniform(0,10) < s*(d-days_rem)*10:
                                    symptomatic[i] = True
                                    symptomatic_nodes.append(i)
                            elif rand.uniform(0,10) < r*10:
                                        recovered[i] = True
                                        rec+=1
                                        recovered_nodes.append(i)
                                        quarantined[i] = False
                                        infected[i] = False
                                        symptomatic[i] = False
                    if symptomatic[i]==True:
                            symptomatic_days[i]+=1
                            if quarantined[i] == False:
                                if rand.uniform(0,10) < h*10:
                                        quarantined[i] = True
                                        quarantined_nodes.append(i)
                            if rand.uniform(0,10) < r*10:
                                        recovered[i] = True
                                        rec+=1
                                        recovered_nodes.append(i)
                                        quarantined[i] = False
                                        infected[i] = False
                                        symptomatic[i] = False
                            if rand.uniform(0,10) < x*10:
                                        deceased[i] = True
                                        dead+=1
                                        deceased_nodes.append(i)
                                        infected[i] = False
                                        symptomatic[i] = False
                                        quarantined[i] = False

                    if quarantined[i] == False and recovered[i] == False and deceased[i] == False:
                        queue.append(i)
            
            numInfected.append(inf)

        colvec = [0]* Gr.number_of_nodes()
        for i in range(Gr.number_of_nodes()):
            if quarantined[i]:
                colvec[i] = 'b'
            elif symptomatic[i]:
                colvec[i] = 'r'
            elif infected[i]:
                colvec[i] = 'y'
            else:
                colvec[i] = 'g'

        #n = nx.draw_networkx(Gr, pos=nx.kamada_kawai_layout(Gr), node_color=colvec, cmap=plt.cm.rainbow, ax = axes[int((d-days_rem-1)/2)][(d-days_rem-1)%2]) #visualizes
        layout = nx.kamada_kawai_layout(Gr)
        nx.draw_networkx_nodes(Gr, pos = layout, node_color = colvec, ax = axes[int((d-days_rem-1)/2)][(d-days_rem-1)%2])
        nx.draw_networkx_edges(Gr, pos = layout, ax = axes[int((d-days_rem-1)/2)][(d-days_rem-1)%2])
        #sm = plt.cm.ScalarMappable(cmap=plt.cm.rainbow, norm = None)
        #m.set_array([])
        #cbar = plt.colorbar(sm)

        plt.figure()
        plt.plot(days, numInfected)
        plt.show()

        return [infected_nodes,quarantined_nodes,symptomatic_nodes,recovered_nodes,deceased_nodes]

print(BFS_t(G,10,0.3,0.9,0.7,0.02,0.001,7))
