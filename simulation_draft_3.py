# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:14:33 2020

@author: Aleksandre
"""

import networkx as nx
import numpy as np
import numpy.random as rand
import random
from collections import deque
import matplotlib.pyplot as plt
import math
import scipy.stats as stats
import operator



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
#G = nx.gnp_random_graph(600,0.1)
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




# x = np.linspace (0, 100, 200)

# y1 = stats.gamma.pdf(x, a=4.94, scale=1/.26)
# plt.plot(x, y1, "y-", label=(r'$\alpha=29, \beta=3$'))


# plt.ylim([0,.2])
# plt.xlim([0,60])
# plt.show()

# y2 = stats.gamma.pdf(x, a=8.16, scale=1/.33)
# plt.plot(x, y2, "y-", label=(r'$\alpha=29, \beta=3$'))


# plt.ylim([0,.2])
# plt.xlim([0,60])
# plt.show()

# y3 = stats.gamma.pdf(x, a=5.81, scale=1/0.95)
# plt.plot(x, y3, "y-", label=(r'$\alpha=29, \beta=3$'))


# plt.ylim([0,.2])
# plt.xlim([0,60])
# plt.show()


output = [0] * G.number_of_nodes()
for i in range(0,G.number_of_nodes()):
    output[i] = rand.random()


def BFS_t(Gr,zero,p,h,d,s,x,r):

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

        #Probability arrays
        death_rate = [x] * Gr.number_of_nodes()
        recovery_rate = [r] * Gr.number_of_nodes()
        symptom_rate = [s] * Gr.number_of_nodes()

        if x < 0:
            for i in range(0,Gr.number_of_nodes()):
                death_rate[i] = 1/np.random.gamma(4.94, 1/.26)
        if r < 0:
            for i in range(0,Gr.number_of_nodes()):
                recovery_rate[i] = 1/np.random.gamma(8.16, 1/.33)
        if s < 0:
            for i in range(0,Gr.number_of_nodes()):
                symptom_rate[i] = 1/np.random.gamma(5.81, 1/0.95)

        #Output array
        GDP_per_capita = 62886.8
        GDP_daily_per_capita = GDP_per_capita / 365
        life_expectancy = 78.6
        hospital_rate = 0.13
        hospital_cost = 14366
        symptom_cost = 3045
        infected_cost = hospital_cost*hospital_rate + symptom_cost*(1-hospital_rate)
        death_cost = 10000000 / (life_expectancy * 365)
        
        
        total_output = 0

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
        num_total_infected    = []
        num_sus = []
        num_new_cases_per_day = []

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
                            if rand.uniform(0,10) < symptom_rate[i]*10:
                                    symptomatic[i] = True
                                    symptomatic_nodes.append(i)
                            elif rand.uniform(0,10) < recovery_rate[i]*10:
                                        recovered[i] = True
                                        rec+=1
                                        inf-=1
                                        recovered_nodes.append(i)
                                        infected[i] = False
                                        symptomatic[i] = False
                                        infected_nodes.remove(i)
                    else:
                            if rand.uniform(0,10) < death_rate[i]*10:
                                        deceased[i] = True
                                        dead+=1
                                        inf-=1
                                        deceased_nodes.append(i)
                                        infected[i] = False
                                        symptomatic[i] = False
                                        symptomatic_nodes.remove(i)
                                        infected_nodes.remove(i)
                            elif rand.uniform(0,10) < recovery_rate[i]*10:
                                        recovered[i] = True
                                        rec+=1
                                        inf-=1
                                        recovered_nodes.append(i)
                                        infected[i] = False
                                        symptomatic[i] = False
                                        symptomatic_nodes.remove(i)
                                        infected_nodes.remove(i)


                    if quarantined[i] == False and recovered[i] == False and deceased[i] == False:
                        queue.append(i)
            for i in range(0,Gr.number_of_nodes()):
                if quarantined[i] == False and deceased[i] == False and symptomatic[i] == False:
                    total_output+=GDP_daily_per_capita
                elif quarantined[i] == True and deceased[i] == False and symptomatic[i] == False:
                    total_output+=0.5*GDP_daily_per_capita
                elif symptomatic[i] == True and deceased[i] == False:
                    total_output-= infected_cost
                elif deceased[i] == True:
                    total_output-= death_cost
            # Update per-day numbers
            num_infected_per_day.append(inf)
            num_symptomatic_per_day.append(len(symptomatic_nodes))
            num_quarantined_per_day.append(len(quarantined_nodes))
            num_recovered_per_day.append(rec)
            num_deceased_per_day.append(dead)
            num_total_infected.append(inf+rec+dead)
            num_sus.append(Gr.number_of_nodes()-inf-rec-dead)
        return [infected_nodes,quarantined_nodes,symptomatic_nodes,recovered_nodes,deceased_nodes, num_infected_per_day, num_quarantined_per_day, num_symptomatic_per_day, num_recovered_per_day, num_deceased_per_day,num_total_infected,num_sus,total_output]

# Returns the average total number of infections per day over n realizations
def plot_numbers_per_day(res, beta, qrnt, days, prefix):
    days_axis = [i for i in range(1, days+1)]
    labels = ["Infected Per Day", "Cumulative Quarantined", "Symptomatic Per Day", "Recovered Per Day", "Deceased Per Day","Total infections","Susceptible"]
    fig = plt.figure()

    fig.suptitle("Beta = " + str(beta) + ", Quarantine Rate = " + str(qrnt), fontsize=12)
    for p in range(len(res)-1):
        ax = fig.add_subplot(111)
        ax.plot(days_axis, res[p], label=labels[p])
        ax.legend(loc="upper right")
        filename = "figure "+ prefix+" " + str(beta) + " " + str(qrnt) +".png"
        plt.savefig(filename, dpi = 500)   
        
def multi_BFS_t(Gr, zero, beta, qrnt, days, s_rate, x_rate, r_rate, n, prefix):
    avg_res_per_day = [[0] * days] * 7

    for i in range(n):
        res = BFS_t(Gr, zero, beta, qrnt, days, s_rate, x_rate, r_rate)[5:12]
        for j in range(len(res)):
            avg_res_per_day[j] = [x + y for x, y in zip(avg_res_per_day[j], res[j])]
            # print(res[j])
            # for k in range(days):
            #     avg_res_per_day[j][k] += res[j][k]

    for l in range(7):
        for m in range(days):
            if avg_res_per_day[l][m] != 0:
                avg_res_per_day[l][m] /= n
    plot_numbers_per_day(avg_res_per_day, beta, qrnt, days, prefix)
    return avg_res_per_day

 
start_random = rand.randint(0,G.number_of_nodes()-1)
starting_node = start_random
r_0 = 2.45
beta = r_0 * 1/24.7
quarantine = 0.3
days = 28
s_rate = -1
r_rate = -1
x_rate = -1

res = BFS_t(G,starting_node,beta,quarantine,days,s_rate,x_rate, r_rate)
#plot_numbers_per_day(res[5:], beta, quarantine, days)
#plt.show()

totals = {}
rand_list = random.sample(range(0, G.number_of_nodes()), 50)
for i in range(1,21):
    avg_out = 0
    for j in range(50):
        avg_out += BFS_t(G,rand_list[j],beta,i/20,days,s_rate,x_rate, r_rate)[12]
    totals[round(i*0.05,2)] = round(avg_out/50,3)


print(sorted(totals.items(), key = operator.itemgetter(1)))
log_fit = np.polyfit(np.log(list(totals.keys())),list(totals.values()),1)
logfig = plt.figure()
logfig.suptitle("Network Value over Quarantine Rates")
ax1 = logfig.add_subplot(111)
ax1.plot(np.log(list(totals.keys())), log_fit[0]*np.log(list(totals.keys())) + log_fit[1])
ax2 = logfig.add_subplot(111)
ax2.plot(np.log(list(totals.keys())),list(totals.values()))
ax2.set_xlabel("Quarantine Rate")
ax2.set_ylabel("Network Cost-Benefit Value")
plt.show()
plt.savefig("Quarantine Log Curve", dpi = 500)  


multi_BFS_t(G,starting_node, beta,0.9,days,s_rate,x_rate, r_rate, 50, "Quarantine 0.9")
plt.show()

# Running multiple realizations
#multi_res = multi_BFS_t(G,starting_node,beta,quarantine,days,s_rate,x_rate, r_rate, 15)
#plot_numbers_per_day(multi_res, beta, quarantine, days)
#plt.show()

"""
for i in range(0,4):
    quarantine = 0.25*i
    closeness_cent= []
    page_cent=[]
    betweenness_cent= []
    
    

    closeness_cent.append(multi_BFS_t(G,maxclose,beta,quarantine,days,s_rate,x_rate, r_rate, 15, "maxclose")[4][days-1])
    closeness_cent.append(multi_BFS_t(G,midclose,beta,quarantine,days,s_rate,x_rate, r_rate, 15, "midclose")[4][days-1])
    closeness_cent.append(multi_BFS_t(G,minclose,beta,quarantine,days,s_rate,x_rate, r_rate, 15, "minclose")[4][days-1])


    betweenness_cent.append(multi_BFS_t(G,maxbet,beta,quarantine,days,s_rate,x_rate, r_rate, 15, "maxbet")[4][days-1])
    betweenness_cent.append(multi_BFS_t(G,midbet,beta,quarantine,days,s_rate,x_rate, r_rate, 15, "midbet")[4][days-1])
    betweenness_cent.append(multi_BFS_t(G,minbet,beta,quarantine,days,s_rate,x_rate, r_rate, 15, "minbet")[4][days-1])

    page_cent.append(multi_BFS_t(G,maxpr,beta,quarantine,days,s_rate,x_rate, r_rate, 15, "maxpr")[4][days-1])
    page_cent.append(multi_BFS_t(G,midpr,beta,quarantine,days,s_rate,x_rate, r_rate, 15, "midpr")[4][days-1])
    page_cent.append(multi_BFS_t(G,minpr,beta,quarantine,days,s_rate,x_rate, r_rate, 15, "minpr")[4][days-1])

   # closeness_cent.append(multi_BFS_t(G,maxclose,beta,quarantine,days,s_rate,x_rate, r_rate, 15)[5][days-1])
  #  closeness_cent.append(multi_BFS_t(G,midclose,beta,quarantine,days,s_rate,x_rate, r_rate, 15)[5][days-1])
   # closeness_cent.append(multi_BFS_t(G,minclose,beta,quarantine,days,s_rate,x_rate, r_rate, 15)[5][days-1])


  #  betweenness_cent.append(multi_BFS_t(G,maxbet,beta,quarantine,days,s_rate,x_rate, r_rate, 15)[5][days-1])
   # betweenness_cent.append(multi_BFS_t(G,midbet,beta,quarantine,days,s_rate,x_rate, r_rate, 15)[5][days-1])
   # betweenness_cent.append(multi_BFS_t(G,minbet,beta,quarantine,days,s_rate,x_rate, r_rate, 15)[5][days-1])

   # page_cent.append(multi_BFS_t(G,maxpr,beta,quarantine,days,s_rate,x_rate, r_rate, 15)[5][days-1])
   # page_cent.append(multi_BFS_t(G,midpr,beta,quarantine,days,s_rate,x_rate, r_rate, 15)[5][days-1])
   # page_cent.append(multi_BFS_t(G,minpr,beta,quarantine,days,s_rate,x_rate, r_rate, 15)[5][days-1])


    print(closeness_cent)
    print(betweenness_cent)
    print(page_cent)

"""



