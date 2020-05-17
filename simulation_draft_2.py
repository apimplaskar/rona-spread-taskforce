# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:14:33 2020

@author: Aleksandre
"""


import networkx as nx
import random as rand


G = nx.gnp_random_graph(100,0.15)
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
            
print(BFS(G,10,0.2))

def BFS_t(Gr,zero,p,d): 
  
        # Mark all the vertices as not visited 
        infected = [False] * Gr.number_of_nodes()
        symptomatic = [False] * Gr.number_of_nodes()
        quarantined = [False] * Gr.number_of_nodes()
        k=1
        days_rem = d
        # Create a queue for BFS 
        queue = [] 
        infected_nodes = []
        # Mark the source node as  
        # visited and enqueue it 
        queue.append(zero) 
        infected[zero] = True
        while days_rem > 0:  
            days_rem-=1
            print("new day ","infected at start ",k)
         
            while queue: 
                s = queue.pop(0) 
                infected_nodes.append(s)
                for i in Gr.neighbors(s): 
                    if infected[i]==False:
                        if rand.uniform(0,10) < p*10:
                            infected[i] = True
                            queue.append(i) 
                            k+=1
                                    
                            
            queue.append(rand.randint(0, len(infected_nodes)))          
        print("inf",k)           
        return infected_nodes
    
print(BFS_t(G,10,0.08,7))    
