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
import scipy.stats

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
            print("day ",(d-days_rem)," infected: ",inf," recovered: ",rec, " deceased: ",dead)
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
                            if rand.uniform(0,10) < s*10:
                                    symptomatic[i] = True
                                    symptomatic_nodes.append(i)
                            elif rand.uniform(0,10) < r*10:
                                        recovered[i] = True
                                        rec+=1
                                        recovered_nodes.append(i)
                                        quarantined[i] = False
                                        infected[i] = False
                                        symptomatic[i] = False
                    else:
                            symptomatic_days[i]+=1
                            if rand.uniform(0,10) < r*10:
                                        recovered[i] = True
                                        rec+=1
                                        recovered_nodes.append(i)
                                        quarantined[i] = False
                                        infected[i] = False
                                        symptomatic[i] = False
                            elif rand.uniform(0,10) < x*10:
                                        deceased[i] = True
                                        dead+=1
                                        deceased_nodes.append(i)
                                        infected[i] = False
                                        symptomatic[i] = False
                                        quarantined[i] = False
                    
                    if quarantined[i] == False and recovered[i] == False and deceased[i] == False:
                        queue.append(i)

                    
        return [infected_nodes,quarantined_nodes,symptomatic_nodes,recovered_nodes,deceased_nodes]

print(BFS_t(G,10,0.3,0.9,0.3,0.02,0.001,28))
