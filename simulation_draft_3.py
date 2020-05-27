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

G = nx.gnp_random_graph(300,0.1)
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
                            if rand.uniform(0,10) < recovery_rate[i]*10:
                                        recovered[i] = True
                                        rec+=1
                                        inf-=1
                                        recovered_nodes.append(i)
                                        infected[i] = False
                                        symptomatic[i] = False
                                        symptomatic_nodes.remove(i)
                                        infected_nodes.remove(i)
                            elif rand.uniform(0,10) < death_rate[i]*10:
                                        deceased[i] = True
                                        dead+=1
                                        inf-=1
                                        deceased_nodes.append(i)
                                        infected[i] = False
                                        symptomatic[i] = False
                                        symptomatic_nodes.remove(i)
                                        infected_nodes.remove(i)

                    if quarantined[i] == False and recovered[i] == False and deceased[i] == False:
                        queue.append(i)

            # Update per-day numbers
            num_infected_per_day.append(inf)
            num_symptomatic_per_day.append(len(symptomatic_nodes))
            num_quarantined_per_day.append(len(quarantined_nodes))
            num_recovered_per_day.append(rec)
            num_deceased_per_day.append(dead)
            num_total_infected.append(inf+rec+dead)
            num_sus.append(Gr.number_of_nodes()-inf-rec-dead)

        return [infected_nodes,quarantined_nodes,symptomatic_nodes,recovered_nodes,deceased_nodes, num_infected_per_day, num_quarantined_per_day, num_symptomatic_per_day, num_recovered_per_day, num_deceased_per_day,num_total_infected,num_sus]

# Returns the average total number of infections per day over n realizations
def multi_BFS_t(Gr, zero, beta, qrnt, days, n):
    avg_res_per_day = [[0] * days] * 11

    for i in range(n):
        print("Simulating realization ", i, "...")
        res = BFS_t(Gr, zero, beta, qrnt, days)
        for j in range(11):
            for k in range(days):
                avg_res_per_day[j][k] += res[j][k]

    for l in range(11):
        avg_res_per_day[l][:] = [x / n for x in avg_res_per_day[l]] 
    
    return avg_res_per_day

def plot_numbers_per_day(res, beta, qrnt, days, s_rate,x_rate, r_rate):
    days_axis = [i for i in range(1, days+1)]
    labels = ["Infected Per Day", "Cumulative Quarantined", "Symptomatic Per Day", "Recovered Per Day", "Deceased Per Day","Total infections","Susceptible"]
    fig = plt.figure()

    fig.suptitle("Beta = " + str(beta) + ", Quarantine Rate = " + str(qrnt), fontsize=12)
    for p in range(len(res)):
        ax = fig.add_subplot(111)
        ax.plot(days_axis, res[p], label=labels[p])
        ax.legend(loc="upper right")


starting_node = 10
beta = 0.1
quarantine = 0.08
days = 60
s_rate = -1
r_rate = -1
x_rate = -1
res = BFS_t(G,starting_node,beta,quarantine,days,s_rate,x_rate, r_rate)


print(res)
plot_numbers_per_day(res[5:], beta, quarantine, days, s_rate,x_rate, r_rate)
print(res[6])
plt.show()