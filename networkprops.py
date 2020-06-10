#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 14:58:47 2020

@author: Aditya
"""
import networkx as nx
import numpy as np
import collections
import matplotlib.pyplot as plt

def cleanGraph(Gr):
    # takes gexf file
    # output: better indexed network, dict of node labels to easier indices
    inds = {}
    for i in list(Gr.nodes):
        inds[i] = Gr.nodes[i]
    Gr = nx.convert_node_labels_to_integers(Gr)
    return Gr, inds

day1 = nx.read_gexf("data/sp_data_school_day_1_g.gexf_")
G, inds = cleanGraph(day1)

degrees = sorted([x for n, x in G.degree()], reverse = True)
degreeCount = collections.Counter(degrees)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color='b')
fig.suptitle("Degree distribution of real world school network")
plt.xlabel("degree")
plt.ylabel("frequency")
plt.savefig("DegreeDist.png", dpi = 500)

neighbor_degs = nx.average_neighbor_degree(G).values()

print("radius: %f" % nx.radius(G))
print("diameter: %f" % nx.diameter(G))
print("average shortest path: %f" % nx.average_shortest_path_length(G))
print("average degree: %f" % np.mean(degrees))
print("average neighbor's degree: %f" % np.mean(list(neighbor_degs)))


"""
radius: 2
diameter: 3
average shortest path: 1
average degree: 49
average neighbor's degree: 55
"""
