# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:14:33 2020

@author: Aleksandre
"""


import networkx as nx
import collections
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import random as rand



with open('D:/Works/Spring20/168/starwars-episode-2-interactions-allCharacters.json') as f:
  data = json.load(f)
  
  

G = nx.node_link_graph(data)
    
color_map = []
names = []


for i in data['nodes']:
    color_map.append(i['colour'])
    names.append(i['name'])
print(len(names))      
DD = nx.degree_histogram(G)
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
# print "Degree sequence", degree_sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())
cnt2 = tuple(ti/len(names) for ti in cnt)

fig, ax = plt.subplots()
plt.figure(figsize=(10, 2))
plt.bar(deg, cnt2, width=0.80, color='b')
plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
ax.set_xticks([d + 0.4 for d in deg])
ax.set_xticklabels(deg)
plt.show()

close_cent = nx.eigenvector_centrality_numpy(G)

charList = pd.DataFrame(data = names, index = close_cent.keys())
centList = pd.DataFrame(data = close_cent.values(), index = close_cent.keys())
masterList = pd.concat([charList, centList],axis=1)
masterList.columns = ['Name','Closeness Centrality']
print(masterList.nlargest(10,'Closeness Centrality'))

nx.draw(G, node_color = color_map, pos = nx.spring_layout(G,k=1,iterations=15), with_labels = True, font_color = "#000000", node_size=[v * 3600 for v in close_cent.values()])

#nx.draw_kamada_kawai(G, node_color = color_map,  with_labels = True, font_color = "#FFFFFF", node_size=[v * 3600 for v in close_cent.values()])
print(nx.degree(G))


print(G.number_of_nodes())
print(rand.uniform(1,10))

inf = [True]*G.number_of_nodes()

def BFS(Gr,zero,p): 
  
        # Mark all the vertices as not visited 
        visited = [False] * Gr.number_of_nodes()
        infected = [False] * Gr.number_of_nodes()
        k=0
  
        # Create a queue for BFS 
        queue = [] 
  
        # Mark the source node as  
        # visited and enqueue it 
        queue.append(zero) 
        visited[zero] = True
        infected[zero] = True
  
        while queue and k < Gr.number_of_nodes()*3: 
            k+=1
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
                    if rand.uniform(1,10) < p*10:
                        infected[i] = True
                        queue.append(i) 
                                    
        #for i in range(0,len(infected)):
          #  if infected[i]==True:
          #      print(i)
                    
            
BFS(G,10,0.25)
