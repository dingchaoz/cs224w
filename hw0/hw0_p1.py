import snap


'''
Problem 1

Load wiki-vote
'''

Gwiki = snap.LoadEdgeList(snap.PNGraph,'wiki-Vote.txt',0,1)

'''
1.1
The number of nodes in network
'''
print 'there are %d nodes' % (Gwiki.GetNodes())


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

CntSelfEdegeNodes(Gwiki)

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

CntDirEdegeNodes(Gwiki)


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

CntUDirEdegeNodes(Gwiki)


'''
1.5
The number of reciprocated edges
'''

def CntRcprEdegeNodes(G):
    UG = snap.ConvertGraph(snap.PUNGraph,G)
    num = G.GetEdges() - UG.GetEdges()

    print 'there are %d reciprocated edge nodes' %(num)
    return num

CntRcprEdegeNodes(Gwiki)


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

Cnt0OutDegNodes(Gwiki)


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

Cnt0InDegNodes(Gwiki)



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

CntMore10InDegNodes(Gwiki)

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

CntFewer10InDegNodes(Gwiki)
