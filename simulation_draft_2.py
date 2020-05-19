# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:14:33 2020

@author: Aleksandre
"""

import networkx as nx
import random as rand
import matplotlib.pyplot as plt

G = nx.gnp_random_graph(1000,0.15)
nx.draw(G)

def BFS(Gr,zero,p): 
  
        # Mark all the vertices as not visited 
        infected = [False] * Gr.number_of_nodes()
        k=1
        # Create a queue for BFS 
        queue = [] 
        infected_nodes = []
        # Mark the source node as  
        # visited and enqueue it 
        queue.append(zero) 
        infected[zero] = True
        
        while queue: 
            
            # Dequeue a vertex from  
            # queue and print it 
            s = queue.pop(0) 
            infected_nodes.append(s)
  
            # Get all adjacent vertices of the 
            # dequeued vertex s. If a adjacent 
            # has not been visited, then mark it 
            # visited and enqueue it 
            for i in Gr.neighbors(s): 
                if infected[i]==False:
                    if rand.uniform(0,10) < p*10:
                        infected[i] = True
                        queue.append(i) 
                        k+=1
                                    
        #for i in range(0,len(infected)):
          #  if infected[i]==True:
          #      print(i)
        print("inf",k)           
        return infected_nodes
            
#print(BFS(G,10,0.2))
#def pBecomeSymptomatic(t):

def BFS_t(Gr,zero,p_symp,p_asymp,p_become_symp,p_qrnt,d):
    days = [i for i in range(1, d+1)]
    numInfected = []
    # Mark all the vertices as not visited
    infected = [False] * Gr.number_of_nodes()
    symptomatic = [False] * Gr.number_of_nodes()
    quarantined = [False] * Gr.number_of_nodes()
    k=1
    days_rem = d
    # Create a queue for BFS
    queue = []
    infected_nodes = []
    symptomatic_nodes = []
    quarantined_nodes = []
    # Mark the source node as
    # visited and enqueue it
    queue.append(zero)
    infected[zero] = True
    infected_nodes.append(zero)
    while days_rem > 0:
        days_rem-=1
        print("day ",(d-days_rem)," infected at start ",k)
        while queue:
            s = queue.pop(0)
            for i in Gr.neighbors(s):
                if infected[i]==False:
                    if symptomatic[s]==True:
                        if rand.uniform(0,10) < p_symp*10:
                            infected[i] = True
                            infected_nodes.append(i)
                            k+=1
                    else:
                        if rand.uniform(0,10) < p_asymp*10:
                            infected[i] = True
                            infected_nodes.append(i)
                            k+=1

        for i in infected_nodes:
            if symptomatic[i] == False:
                    if rand.uniform(0,10) < p_become_symp*(d-days_rem)*10:
                            symptomatic[i] = True
                            symptomatic_nodes.append(i)
            if symptomatic[i]==True and quarantined[i] == False:
                    if rand.uniform(0,10) < p_qrnt*10:
                            quarantined[i] = True
                            quarantined_nodes.append(i)

            if quarantined[i] == False:
                queue.append(i)
        
        numInfected.append(k)

    plt.figure()
    plt.plot(days, numInfected)
    plt.show()
    print("inf",k)
    return [infected_nodes,quarantined_nodes,symptomatic_nodes]

print(BFS_t(G,10,0.2,0.1,0.495,0.7,7)) 