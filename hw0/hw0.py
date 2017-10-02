import snap
import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import os
os.chdir('')
'''
Problem 1

Construct directed Gsmall = (Vsmall, Esmall)
Vsmall = {1,2,3}
Esmall = {(1,2),(2,1),(1,3),(1,1)}
'''

Gsmall = snap.TNGraph.New()

Gsmall.AddNode(1)
Gsmall.AddNode(2)
Gsmall.AddNode(3)

Gsmall.AddEdge(1,2)
Gsmall.AddEdge(2,1)
Gsmall.AddEdge(1,3)
Gsmall.AddEdge(1,1)

'''
1.1
The number of nodes in network
'''
print 'there are %d nodes' % (Gsmall.GetNodes())


'''
1.2
The number of nodes with a self-edge
'''

def CntSelfEdegeNodes(G):
    num = 0
    for EI in G.Edges():
        if EI.GetSrcNId() == EI.GetDstNId():
            num +=1
    print 'there are %d self-edge nodes' %(num)
    return num

CntSelfEdegeNodes(Gsmall)

'''
1.3
The number of directed edges
'''

def CntDirEdegeNodes(G):
    num = 0
    for EI in G.Edges():
        if EI.GetSrcNId() != EI.GetDstNId():
            num +=1
    print 'there are %d directed edge nodes' %(num)
    return num

CntDirEdegeNodes(Gsmall)


'''
1.4
The number of undirected edges
'''

def CntUDirEdegeNodes(G):
    UG = snap.ConvertGraph(snap.PUNGraph,G)
    num = 0
    for EI in UG.Edges():
        if EI.GetSrcNId() != EI.GetDstNId():
            num +=1
    print 'there are %d undirected edge nodes' %(num)
    return num

CntUDirEdegeNodes(Gsmall)


'''
1.5
The number of reciprocated edges
'''

def CntRcprEdegeNodes(G):
    UG = snap.ConvertGraph(snap.PUNGraph,G)
    num = G.GetEdges() - UG.GetEdges()

    print 'there are %d reciprocated edge nodes' %(num)
    return num

CntRcprEdegeNodes(Gsmall)


'''
1.6
The number of nodes of zero out-degree

'''
def Cnt0OutDegNodes(G):
    num = 0
    for NI in G.Nodes():
        if NI.GetOutDeg() == 0:
            num +=1
    print 'there are %d nodes of zero out-degree' %(num)
    return num

Cnt0OutDegNodes(Gsmall)


'''
1.7
The number of nodes of zero in-degree

'''
def Cnt0InDegNodes(G):
    num = 0
    for NI in G.Nodes():
        if NI.GetInDeg() == 0:
            num +=1
    print 'there are %d nodes of zero in-degree' %(num)
    return num

Cnt0InDegNodes(Gsmall)



'''
1.8
The number of nodes with more than 10 incoming edges

'''
def CntMore10InDegNodes(G):
    num = 0
    for NI in G.Nodes():
        if NI.GetInDeg() >= 10:
            num +=1
    print 'there are %d nodes with more than 10 incoming edges' %(num)
    return num

CntMore10InDegNodes(Gsmall)

'''
1.9
The number of nodes with fewer than 10 incoming edges

'''
def CntFewer10InDegNodes(G):
    num = 0
    for NI in G.Nodes():
        if NI.GetInDeg() < 10:
            num +=1
    print 'there are %d nodes with fewer than 10 incoming edges' %(num)
    return num

CntFewer10InDegNodes(Gsmall)

'''
Problem 2
'''

Gwiki = snap.LoadEdgeList(snap.PNGraph,'cs224w/hw0/wiki-Vote.txt',0,1)

'''
2.1
Out-degree distribution plotting on log-log scale
'''

odegree_list = []

for NI in Gwiki.Nodes():
    odegree_list.append(NI.GetOutDeg())

hist = np.histogram(odegree_list,bins=range(len(odegree_list)))
hist_nonzero = [(x,y) for (x,y) in zip(hist[0],hist[1]) if x > 0]
X = [x for x,y in hist_nonzero]
Y = [y for x,y in hist_nonzero]
logX = np.log10(X)
logY = np.log10(Y)
plt.plot(logX,logY)


'''
Compute and plot least-square regression line
Use numpy polyfit with deg == 1 ?
'''
idx = np.isfinite(logX) & np.isfinite(logY)
coefficients = np.polyfit(logX[idx], logY[idx], 1)

#coefficients = np.polyfit(logY, logX, 1)
polynomial = np.poly1d(coefficients)
ys = polynomial(logX)
plt.plot(logY, logX)
plt.plot(logX, ys)


'''
Problem 3
'''


'''
3.1
Number of weakly connected components using GetWccs
'''
Gstack= snap.LoadEdgeList(snap.PNGraph,'cs224w/hw0/stackoverflow-Java.txt',0,1)
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
