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
        visited = [False] * Gr.number_of_nodes()
        infected = [False] * Gr.number_of_nodes()
        k=1
  
        # Create a queue for BFS 
        queue = [] 
  
        # Mark the source node as  
        # visited and enqueue it 
        queue.append(zero) 
        visited[zero] = True
        infected[zero] = True
  
        while queue: 
            
            # Dequeue a vertex from  
            # queue and print it 
            s = queue.pop(0) 
            print (s, end = " ") 
  
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
            
BFS(G,10,0.2)
