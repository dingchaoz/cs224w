import snap
import numpy as np
import collections

"""
P3.1

"""

'''
load 2 graphs
'''

G1 = snap.LoadEdgeList(snap.PUNGraph, 'graph1.txt', 0, 1)
G2 = snap.LoadEdgeList(snap.PUNGraph, 'graph2.txt', 0, 1)


'''
initialize vectors storing voting status
at each iteration
'''


# 1 for A, -1 for B , 0 for undecided
V0_G1 = [1 if str(i)[-1] <= '3' else 0 if str(i)[-1] >= '8' else -1 for i in range(10000)] #initial voting before any iteration
V0_G2 = V0_G1[:] #initial voting before any iteration

'''
10 basic iteration process
'''

undecided_nodes = [i for i in range(10000) if str(i)[-1] >= '8'] # undecided nodes id


def decision_simulation(G,V0,undecided_nodes):

    '''
    G1: Graph
    V0_G1: initial vote status
    undecided_nodes: nodes which will be impacted

    return: votes_alliterations result
    '''

    alternate = 1 # alternative value assignment to undecided node
    votes_alliterations = [] # an array holding all voting status in each iteration
    votes_alliterations.append(V0) # add initial status to the holding array

    for i in range(10):

        print 'starting decision process at iteration %i' %i

        V_prev = votes_alliterations[i] # get last iteration's voting status

        V_curr = V_prev # start with this iteration

        for node in undecided_nodes: # iterating only undecided nodes

            NI = G.GetNI(node) # get the node id

            print 'iterating node %i' % node

            neibhor_votes = [] # array holding the neibor nodes' voting status

            for Id in NI.GetOutEdges():

                # neighbor node is Id and count the majority, do this search using current iteration voting status
                neibhor_votes.append(V_curr[Id])

                print 'neibor voted %i' %V_curr[Id]

            count = collections.Counter(neibhor_votes)
            if count[1] > count[-1]:

                V_curr[node] = 1

                print 'more neibgor voted 1'

            elif count[-1] > count[1]:

                V_curr[node] = -1

                print 'more neibgor voted -1'

            elif count[-1] == count[1]:

                V_curr[node] = alternate

                print 'neibgor vote equal, assign this node vote %i' %alternate

            alternate *= -1

            print 'alternate assign value'

        votes_alliterations.append(V_curr)

        print 'iteration %i finished, append the voting results' %i


    final_vote_G = votes_alliterations[-1]
    G_final_count = collections.Counter(final_vote_G)
    print 'In Graph there are %i voters for A' %G_final_count[1]
    print 'In Graph there are %i voters for B' %G_final_count[-1]

    return votes_alliterations

votes_alliterations_G1 = decision_simulation(G1,V0_G1,undecided_nodes)
'''
In Graph there are 4934 voters for A
In Graph there are 5066 voters for B
'''

votes_alliterations_G2 = decision_simulation(G2,V0_G2,undecided_nodes)
'''
In Graph 2 there are 4882 voters for A
In Graph 2 there are 5118 voters for B

'''


"""
P3.2

"""

# 1 for A, -1 for B , 0 for undecided
V0_G1 = [1 if str(i)[-1] <= '3' else 0 if str(i)[-1] >= '8' else -1 for i in range(10000)] #initial voting before any iteration
V0_G2 = V0_G1[:] #initial voting before any iteration

'''
10 basic iteration process
'''

def compute_ads_nodes(k):

    ads_nodes = range(3000,3000+k/100-1)

    return ads_nodes

undecided_nodes = [i for i in range(10000) if str(i)[-1] >= '8'] # undecided nodes id

G1_results_ads =[]
G2_results_ads = []

for k in range(1000,10000,1000):

    print 'spending %i dollars ' %k

    ads_nodes = compute_ads_nodes(k)

    print 'ads affected nodes are: ',ads_nodes

    undecided_nodes_after_ads = [x for x in undecided_nodes if x not in ads_nodes]

    V0_G1_after_ads = V0_G1[:]
    V0_G2_after_ads = V0_G2[:]

    for i in ads_nodes:
        V0_G1_after_ads[i] = 1
        V0_G2_after_ads[i] = 1

    votes_alliterations_G1_afterads = decision_simulation(G1,V0_G1_after_ads,undecided_nodes_after_ads)
    votes_alliterations_G2_afterads = decision_simulation(G2,V0_G2_after_ads,undecided_nodes_after_ads)

    final_vote_G1 = votes_alliterations_G1_afterads[-1]
    G1_final_count = collections.Counter(final_vote_G1)
    G1_A = G1_final_count[1]
    G1_B = G1_final_count[-1]
    G1_results_ads.append((G1_A,G1_B))

    final_vote_G2 = votes_alliterations_G2_afterads[-1]
    G2_final_count = collections.Counter(final_vote_G2)
    G2_A = G2_final_count[1]
    G2_B = G2_final_count[-1]
    G2_results_ads.append((G2_A,G2_B))

'''
In[108]: G1_results_ads
Out[108]:
[(4926, 5074),
 (4936, 5064),
 (4940, 5060),
 (4946, 5054),
 (4954, 5046),
 (4965, 5035),
 (4973, 5027),
 (4983, 5017),
 (4995, 5005)]
In[109]: G2_results_ads
Out[109]:
[(4860, 5140),
 (4884, 5116),
 (4898, 5102),
 (4908, 5092),
 (4917, 5083),
 (4940, 5060),
 (4951, 5049),
 (4961, 5039),
 (4970, 5030)]
'''


"""
3.3

"""
'''
Get top 9 highest degree nodes
'''

def getTop9DegNodes(G):
    allnodes_degree = {}
    for NI in G.Nodes():
        print "node: %d, out-degree %d" % ( NI.GetId(), NI.GetOutDeg())
        allnodes_degree[NI.GetId()] = NI.GetOutDeg()

    alldegrees = [value for key, value in allnodes_degree.iteritems()]
    alldegrees.sort()
    top9degrees = alldegrees[-9:]
    set_top9_degrees = list(set(top9degrees))
    set_top9_degrees.sort(reverse=True)
    allnodes_degree.keys()[allnodes_degree.values().index(10)]
    l = []

    for i in set_top9_degrees:
       ll = [k for k,v in allnodes_degree.iteritems() if v == i]
       l.append(ll)

    top9degree_indicis = [item for sublist in l for item in sublist][:9]

    top9degrees.reverse()

    return top9degree_indicis,top9degrees

top9degree_indicis_G1,top9degrees_G1 = getTop9DegNodes(G1)
# [354, 896, 7035, 682, 804, 1878, 3685, 5190, 2704] --> [38, 38, 38, 36, 36, 36, 36, 36, 35]
top9degree_indicis_G2,top9degrees_G2 = getTop9DegNodes(G2)
# [12, 11, 10, 17, 16, 15, 6, 26, 18] --> [527, 505, 445, 416, 406, 389, 358, 349, 346]

'''
decision process

'''

V0_G1 = [1 if str(i)[-1] <= '3' else 0 if str(i)[-1] >= '8' else -1 for i in range(10000)] #initial voting before any iteration
V0_G2 = V0_G1[:] #initial voting before any iteration

undecided_nodes = [i for i in range(10000) if str(i)[-1] >= '8'] # undecided nodes id

G1_results_ads =[]
G2_results_ads = []

for k in range(1000,10000,1000):

    print 'spending %i dollars ' %k

    highroll_nodes_G1 = top9degree_indicis_G1[:k/1000]
    highroll_nodes_G2 = top9degree_indicis_G2[:k/1000]

    print 'dinner affected nodes in G1 are: ',highroll_nodes_G1
    print 'dinner affected nodes in G2 are: ',highroll_nodes_G2

    undecided_nodes_after_ads_G1 = [x for x in undecided_nodes if x not in highroll_nodes_G1]
    undecided_nodes_after_ads_G2 = [x for x in undecided_nodes if x not in highroll_nodes_G2]

    V0_G1_after_ads = V0_G1[:]
    V0_G2_after_ads = V0_G2[:]

    for i in highroll_nodes_G1:
        print 'G1', i
        V0_G1_after_ads[i] = 1

    for i in highroll_nodes_G2:
        print 'G2', i
        V0_G2_after_ads[i] = 1

    votes_alliterations_G1_afterads = decision_simulation(G1,V0_G1_after_ads,undecided_nodes_after_ads_G1)
    votes_alliterations_G2_afterads = decision_simulation(G2,V0_G2_after_ads,undecided_nodes_after_ads_G2)

    final_vote_G1 = votes_alliterations_G1_afterads[-1]
    G1_final_count = collections.Counter(final_vote_G1)
    G1_A = G1_final_count[1]
    G1_B = G1_final_count[-1]
    G1_results_ads.append((G1_A,G1_B))

    final_vote_G2 = votes_alliterations_G2_afterads[-1]
    G2_final_count = collections.Counter(final_vote_G2)
    G2_A = G2_final_count[1]
    G2_B = G2_final_count[-1]
    G2_results_ads.append((G2_A,G2_B))

'''

In[52]:

G1_results_ads
[(4941, 5059),
 (4947, 5053),
 (4955, 5045),
 (4955, 5045),
 (4957, 5043),
 (4981, 5019),
 (4982, 5018),
 (4982, 5018),
 (4983, 5017)]

G2_results_ads

Out[52]:

 [(4882, 5118),
 (4882, 5118),
 (4882, 5118),
 (4917, 5083),
 (4970, 5030),
 (5000, 5000),
 (5038, 4962),
 (5086, 4914),
 (5104, 4896)]
'''





