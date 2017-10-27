'''
calculate the degree sequence of the real world network by creating a vector k = [k1,k2,k3..ki...kn]
 where ki is the degree of node i and n is the number of nodes in the graph.

'''

import snap
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt



powergraph = snap.LoadEdgeList(snap.PUNGraph, 'USpowergrid_n4941.txt', 0, 1)
k = []

for NI in powergraph.Nodes():
    k.append(NI.GetOutDeg())

'''
create an array v and fill it by writing the index i exactly ki times for each element in
the degree sequence. Each of these i's represents a stub of the ith node in the graph.
'''

v_temp = [[i+1]*x for i,x in enumerate(k)]
v = [item for sublist in v_temp for item in sublist]






'''
create a random network by connecting adjacent pairs in v with an edge.
if contains self edge or multi edge, stop the creation
'''

def create_random_net(v):
    N = np.max(v)
    Graph = snap.TUNGraph.New()

    # Add nodes
    for i in range(1,N+1):
        Graph.AddNode(i)

    #randomly permute the elements of v
    shuffle(v)
    for i in range(0,len(v)-1,2):

        if v[i] != v[i+1] and not Graph.IsEdge(v[i],v[i+1]):
            Graph.AddEdge(v[i],v[i+1])
        else:
            break

    return Graph


'''
create 100 sampled random network, if the number of edges of created sample network is not equal to the us
powergrid net's number of edges, don't count this

'''

networks = []
needed_edges = powergraph.GetEdges()

while len(networks) < 100:

    g = create_random_net(v)
    if g.GetEdges() == needed_edges:
        networks.append(g)
        print 'added a network'
    else:
        print 'not add this network'


'''
1.1
(a) [10 points] Draw 100 random (simple) network samples using the stub-matching algorithm
using the degree sequence of the power grid network. Calculate the average clustering coe-
cient of each of these samples and report the mean value across samples.

'''

# average cluster coefficient of 100 random networks is 0.000471
# original cluster coefficient of powergraph is 0.08010361108159704
print 'average cluster coefficient of 100 random networks is %f' % (np.mean([snap.GetClustCf(x, -1) for x in networks]))



'''
1.2
Randomly select two distinct edges e1 = (a; b) and e2 = (c; d) from the graph. We will try to
re-wire these edges.
2. Randomly select one of endpoint of edge e1 and call it u. Let v be the other endpoint in
e1. At this point, either u = a, v = b or u = b, v = a. Do the same for edge e2. Call the
randomly selected endpoint w and the other endpoint x.
3. Perform the rewiring. In the graph, replace the undirected edges e1 = (a; b) and e2 = (c; d)
with the undirected edges (u;w) and (v; x) as long as this results in a simple network (no
self-loops or multi-edges). If the result is not a simple network, reject this rewiring and return
to step 1; otherwise, keep the newly swapped edges and return to step 1.
'''

edge_list = [EI.GetId() for EI in powergraph.Edges()]


def rewire(edge_list,powergraph):

    iteration = 0
    clcoeff_arr = []

    while iteration < 10000:

        # select 2 edges e_1, e_2 which are composed of sourcing and destination nodes
        e_1, e_2 = np.random.choice(len(edge_list),2)
        # decide a, b which one goes to u or v
        r = np.random.choice([0,1],2,replace= False)
        # assign u, v to a, b or b,a
        u,v = [edge_list[e_1][r[0]],edge_list[e_1][r[1]]]
        # decide c, d which one goes to w or x
        r = np.random.choice([0,1],2,replace= False)
        # assign w, x to c, d or d,c
        w,x = [edge_list[e_2][r[0]],edge_list[e_2][r[1]]]

        # intend to rewire
        if u != w and not Graph.IsEdge(u,w):
            powergraph.AddEdge(u,w)
        else:
            print 'abort and rewire'
            continue
        if v != x and not Graph.IsEdge(v,x):
            powergraph.AddEdge(v,x)
        else:
            print 'abort and rewire'
            continue


        # delete edge e_1 and e_2
        powergraph.DelEdge(edge_list[e_1][0],edge_list[e_1][1])
        powergraph.DelEdge(edge_list[e_2][0],edge_list[e_2][1])

        print 'rewire successfully'
        iteration = iteration + 1

        if iteration % 100 == 0:
            clcoeff = snap.GetClustCf(powergraph, -1)
            print 'cluster coefficient at this stage is %f' %(clcoeff)
            clcoeff_arr.append(clcoeff)

    return powergraph,clcoeff_arr

rewired_powergraph,clcoeff_arr =  rewire(edge_list,powergraph)

plt.plot(clcoeff_arr)
plt.xlabel('Iteration every 100 ')
plt.ylabel('Cluster coefficient')
plt.title('Cluster coefficiet in rewiring iteration')
plt.legend()
plt.show()