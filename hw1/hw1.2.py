import snap
import os
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt

os.chdir('/Users/ejlq/Documents/dingchao/school/stanford/cs224w/HW/cs224w/hw1')

'''
load directed edge list
'''
Epinions = snap.LoadEdgeList(snap.PNGraph, 'soc-Epinions1.txt', 0, 1, '\t')
Emails = snap.LoadEdgeList(snap.PNGraph, 'Email-EuAll.txt', 0, 1, '\t')

'''
get max scc and nodes list of each graph
'''
EpiMxScc = snap.GetMxScc(Epinions)
EmailMxScc = snap.GetMxScc(Emails)

EpiMxScc_nodes = [x.GetId() for x in EpiMxScc.Nodes()]
EmailMxScc_nodes = [x.GetId() for x in EmailMxScc.Nodes()]

'''
BFS on forward and backward computing
'''

'''
forward bfs trees and nodes list
'''
EpiBfsTreeOut_9809 = snap.GetBfsTree(Epinions, 9809, True, False)
EpiBfsTreeOut_1952 = snap.GetBfsTree(Epinions, 1952, True, False)
EpiBfsTreeOut_1952_nodes = [x.GetId() for x in EpiBfsTreeOut_1952.Nodes()]
EpiBfsTreeOut_9809_nodes = [x.GetId() for x in EpiBfsTreeOut_9809.Nodes()]

EmailBfsTreeOut_189587 = snap.GetBfsTree(Emails, 189587, True, False)
EmailBfsTreeOut_675 = snap.GetBfsTree(Emails, 675, True, False)
EmailBfsTreeOut_189587_nodes = [x.GetId() for x in EmailBfsTreeOut_189587.Nodes()]
EmailBfsTreeOut_675_nodes = [x.GetId() for x in EmailBfsTreeOut_675.Nodes()]
'''
backward bfs trees and nodes list
'''
EpiBfsTreeIn_9809 = snap.GetBfsTree(Epinions, 9809, False, True)
EpiBfsTreeIn_1952 = snap.GetBfsTree(Epinions, 1952, False, True)
EpiBfsTreeIn_1952_nodes = [x.GetId() for x in EpiBfsTreeIn_1952.Nodes()]
EpiBfsTreeIn_9809_nodes = [x.GetId() for x in EpiBfsTreeIn_9809.Nodes()]

EmailBfsTreeIn_189587 = snap.GetBfsTree(Emails, 189587, False, True)
EmailBfsTreeIn_675 = snap.GetBfsTree(Emails, 675, False, True)
EmailBfsTreeIn_189587_nodes = [x.GetId() for x in EmailBfsTreeIn_189587.Nodes()]
EmailBfsTreeIn_675_nodes = [x.GetId() for x in EmailBfsTreeIn_675.Nodes()]


'''
2.1
'''

print 'There are %i nodes intersecting Epinion Max Scc Component and Node 9809 forward link BFS Tree'\
      % (len(set(EpiMxScc_nodes).intersection(set(EpiBfsTreeOut_9809_nodes))))

print 'There are %i nodes intersecting Epinion Max Scc Component and Node 9809 backward link BFS Tree'\
% (len(set(EpiMxScc_nodes).intersection(set(EpiBfsTreeIn_9809_nodes))))

print 'Node 9809 is a part of the Out component'

print 'There are %i nodes intersecting Epinion Max Scc Component and Node 1952 forward link BFS Tree'\
      % (len(set(EpiMxScc_nodes).intersection(set(EpiBfsTreeOut_1952_nodes))))

print 'There are %i nodes intersecting Epinion Max Scc Component and Node 1952 backward link BFS Tree'\
% (len(set(EpiMxScc_nodes).intersection(set(EpiBfsTreeIn_1952_nodes))))

print 'Node 1952 is a part of the In component'

print 'There are %i nodes intersecting Epinion Max Scc Component and Node 189587 forward link BFS Tree'\
      % (len(set(EmailMxScc_nodes).intersection(set(EmailBfsTreeOut_189587_nodes))))

print 'There are %i nodes intersecting Epinion Max Scc Component and Node 189587 backward link BFS Tree'\
% (len(set(EmailMxScc_nodes).intersection(set(EmailBfsTreeIn_189587_nodes))))

print 'Node 189587 is a part of the SCC component'


print 'There are %i nodes intersecting Epinion Max Scc Component and Node 675 forward link BFS Tree'\
      % (len(set(EmailMxScc_nodes).intersection(set(EmailBfsTreeOut_675_nodes))))

print 'There are %i nodes intersecting Epinion Max Scc Component and Node 675 backward link BFS Tree'\
% (len(set(EmailMxScc_nodes).intersection(set(EmailBfsTreeIn_675_nodes))))

print 'Node 675 is a part of the Out component'

'''
2.2
'''

def Bfs_Nodes_Cnt(graph,nodeid,forward=True):

    BfsTree = snap.GetBfsTree(graph, nodeid, forward, not forward)
    BfsTree_nodescnt = BfsTree.GetNodes()

    return BfsTree_nodescnt

Epi_Fwd_Bfs_NodeCnt = []
Epi_Bck_Bfs_NodeCnt = []
Rnd = snap.TRnd(42)
Rnd.Randomize()
for i in range(0,100):
    NID = Epinions.GetRndNId(Rnd)
    Epi_Fwd_Bfs_NodeCnt.append(Bfs_Nodes_Cnt(Epinions,NID,forward=True))
    Epi_Bck_Bfs_NodeCnt.append(Bfs_Nodes_Cnt(Epinions,NID,forward=False))

Email_Fwd_Bfs_NodeCnt = []
Email_Bck_Bfs_NodeCnt = []
Rnd = snap.TRnd(43)
Rnd.Randomize()
for i in range(0,100):
    NID = Emails.GetRndNId(Rnd)
    Email_Fwd_Bfs_NodeCnt.append(Bfs_Nodes_Cnt(Emails,NID,forward=True))
    Email_Bck_Bfs_NodeCnt.append(Bfs_Nodes_Cnt(Emails,NID,forward=False))

'''
Sort
'''
Epi_Fwd_Bfs_NodeCnt.sort()
Epi_Bck_Bfs_NodeCnt.sort()
Email_Fwd_Bfs_NodeCnt.sort()
Email_Bck_Bfs_NodeCnt.sort()



fig = plt.figure(1, (7,4))
ax = fig.add_subplot(1,1,1)

ax.plot(perc, Epi_Fwd_Bfs_NodeCnt)

fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.xaxis.set_major_formatter(xticks)
plt.title('Reachability of Epinions network using outwardlinks')
plt.xlabel('fraction of starting nodes')
plt.ylabel('number of nodes reached')
plt.show()

fig = plt.figure(1, (7,4))
ax = fig.add_subplot(1,1,1)

ax.plot(perc, Epi_Bck_Bfs_NodeCnt)

fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.xaxis.set_major_formatter(xticks)
plt.title('Reachability of Epinions network using inwardlinks')
plt.xlabel('fraction of starting nodes')
plt.ylabel('number of nodes reached')
plt.show()

fig = plt.figure(1, (7,4))
ax = fig.add_subplot(1,1,1)

ax.plot(perc, Email_Fwd_Bfs_NodeCnt)

fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.xaxis.set_major_formatter(xticks)
plt.title('Reachability of Emails network using outwardlinks')
plt.xlabel('fraction of starting nodes')
plt.ylabel('number of nodes reached')
plt.show()

fig = plt.figure(1, (7,4))
ax = fig.add_subplot(1,1,1)

ax.plot(perc, Email_Bck_Bfs_NodeCnt)

fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
xticks = mtick.FormatStrFormatter(fmt)
ax.xaxis.set_major_formatter(xticks)
plt.title('Reachability of Emails network using inwardlinks')
plt.xlabel('fraction of starting nodes')
plt.ylabel('number of nodes reached')
plt.show()


'''
2.3
'''
WCC_Components = snap.TCnComV()
snap.GetWccs(Emails, WCC_Components)

for x in WCC_Components:
    print x.Len()

SCC_Components = snap.TCnComV()
snap.GetSccs(Emails, SCC_Components)

for x in Components:
    print x.Len()


EmailMxScc.GetNodes() #34203
WCC_Components[0].Len() #224832
SCC_Components[0].Len() #34203

def Components_compute(graph):

    total_size = graph.GetNodes()

    WCC_Components = snap.TCnComV()
    snap.GetWccs(graph, WCC_Components)
    largest_wcc_size = WCC_Components[0].Len()

    disconnected_size = total_size - largest_wcc_size
    num_disconnected_components = WCC_Components.Len() - 1
    print 'Disconnected components have %i nodes in total' % disconnected_size
    print 'There are %i total disconnected clusters' % num_disconnected_components

    scc_component = snap.GetMxScc(graph)
    scc_nodes = [x.GetId() for x in scc_component.Nodes()]
    scc_size =  scc_component.GetNodes()
    print 'SCC contains %i nodes' % (scc_size)

    '''
    Get a random node from SCC and perform BFS on inward and outward directions
    '''
    Rnd = snap.TRnd(42)
    Rnd.Randomize()
    NID = scc_component.GetRndNId(Rnd)

    BfsTree_Out = snap.GetBfsTree(graph, NID, True, False)
    BfsTree_Out_nodes = [x.GetId() for x in BfsTree_Out.Nodes()]

    BfsTree_In = snap.GetBfsTree(graph, NID, False, True)
    BfsTree_In_nodes = [x.GetId() for x in BfsTree_In.Nodes()]

    '''
    Subtract the SCC nodes from BFS trees we got In and Out components nodes
    '''

    out_size = len(set(BfsTree_Out_nodes) - set(scc_nodes))
    print 'Out component contains %i nodes' % (out_size)

    in_size = len(set(BfsTree_In_nodes) - set(scc_nodes))
    print 'In component contains %i nodes' % (in_size)

    '''
    largest WCC - SCC - In - Out == Tendrills
    '''
    tendrills_size = largest_wcc_size - scc_size - in_size - out_size
    print 'Tendrills contains %i nodes' % (tendrills_size)

Components_compute(Emails)
'''
Disconnected components have 40382 nodes in total
There are 15835 total disconnected clusters
SCC contains 34203 nodes
Out component contains 17900 nodes
In component contains 151023 nodes
Tendrills contains 21706 nodes
'''

Components_compute(Epinions)

'''
Disconnected components have 2 nodes in total
There are 1 total disconnected clusters
SCC contains 32223 nodes
Out component contains 15453 nodes
In component contains 24236 nodes
Tendrills contains 3965 nodes
'''
