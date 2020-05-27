#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 16:32:25 2020

@author: Aditya
"""
import networkx as nx

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

pagerank = nx.pagerank(G)
bet = nx.betweenness_centrality(G)
close = nx.closeness_centrality(G)

def getMaxMinMid(centralities):
    # returns node label for max, min, mid
    import operator
    length = len(centralities)
    nodelist = list(sorted(centralities.items(), key = operator.itemgetter(1)))
    
    mmax = nodelist[length-1][0] 
    mmin = nodelist[0][0]    
    mmid = nodelist[int(length/2)][0]
    
    return mmax, mmin, mmid

maxpr, minpr, midpr = getMaxMinMid(pagerank)
maxbet, minbet, midbet = getMaxMinMid(bet)
maxclose, minclose, midclose = getMaxMinMid(close)

print("Pagerank max:", maxpr, "| Pagerank min:", minpr, "| Pagerank mid:", midpr)
print("Betweenness max:", maxbet, "| Betweenness min:", minbet, "| Betweenness mid:", midbet)
print("Closeness max:", maxclose, "| Closeness min:", minclose, "| Closeness mid:", midclose)

"""
Pagerank max: 136 | Pagerank min: 23 | Pagerank mid: 223
Betweenness max: 7 | Betweenness min: 23 | Betweenness mid: 183
Closeness max: 179 | Closeness min: 23 | Closeness mid: 186
"""
