import snap
import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt

'''
Problem 3
'''


'''
3.1
Number of weakly connected components using GetWccs
'''
Gstack= snap.LoadEdgeList(snap.PNGraph,'stackoverflow-Java.txt',0,1)
Components = snap.TCnComV()
snap.GetWccs(Graph, Components)
for CnCom in Components:
    print "Size of component: %d" % CnCom.Len()
'''
3.2
The largest weakly connected component using GetMxWcc
'''
MxWcc = snap.GetMxWcc(Gstack)

print "there are %d nodes and %d edges in the larges Wcc" % (MxWcc.GetNodes(), MxWcc.GetEdges())


'''
3.3
The top 3 most central nodes in the network by PagePank scores. using GetPageRank
'''
PRankH = snap.TIntFltH()
snap.GetPageRank(Gstack, PRankH)
node_list = []
prscore_list = []
for item in PRankH:
    node_list.append(item)
    prscore_list.append(PRankH[item])

top3_idx = np.array(prscore_list).argsort()[-3:]
top3_nodes = [node_list[i] for i in top3_idx]

print 'top 3 nodes are:', top3_nodes




'''
3.4
The top 3 hubs and top 3 authorities in the network by HITS scores using GetHits
'''

NIdHubH = snap.TIntFltH()
NIdAuthH = snap.TIntFltH()
snap.GetHits(Gstack, NIdHubH, NIdAuthH)
hub_list = []
hub_hitscore_list = []
aut_list = []
aut_hitscore_list = []
for item in NIdHubH:
    hub_list.append(item)
    hub_hitscore_list.append(NIdHubH[item])

for item in NIdAuthH:
    aut_list.append(item)
    aut_hitscore_list.append(NIdAuthH[item])

top3_idx = np.array(hub_hitscore_list).argsort()[-3:]
top3_hubs = [hub_list[i] for i in top3_idx]
print 'top 3 hubs are:', top3_nodes

top3_idx = np.array(aut_hitscore_list).argsort()[-3:]
top3_auts = [node_list[i] for i in top3_idx]
print 'top 3 authorities are:', top3_auts
