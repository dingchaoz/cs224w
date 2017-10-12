################################################################################
# CS 224W (Fall 2017) - HW1
# Starter code for Problem 3.3
# Author: anunay@stanford.edu, tonyekim@stanford.edu
# Last Updated: Oct 7, 2017
################################################################################

import snap
import numpy as np
import sys
import math
import random
import matplotlib.pyplot as plt

# Setup
hT = 10
b = 2
k = 5


def sampleNodes():
  """
  return type: [[int, int]]
  return: An array of pairs of nodes
  """
  ret = []

  i = 0
  while (i < 1000):
    v = random.randint(0, (b ** hT)-1)
    w = random.randint(0, (b ** hT)-1)
    if (v != w):
      ret.append([v,w])
      i += 1

  return ret


def hue(v, w):
  """
  :param - v: node id
  :param - w: node id

  return type: int
  return: h(v, w)
  """
  if (v == w):
    return 0
  else:
    xor = bin(v ^ w)[2:]
    xor = ("0" * (hT - len(xor))) + xor
    return hT - xor.find('1')


def search(Graph, s, t):
  """
  :param - s: node id
  :param - t: node id

  return type: Boolean, Int
  return: After performing the search, return either (True, <distance>) if a
  path is found or (False, -1) otherwise.




  """

  ############################################################################
  # TODO: Your code here!

  # Get out connected nodes of s
  # While the current nodes neighbors h(s,t) > its own distance
  # also check

  steps = 0
  next_node = s
  min_h = 10
  h_st = 11

  print 's and t are %i %i and their h is %f' %(s,t, hue(s,t))

  ## Starting from the initial s node to start search

  while min_h< h_st:

    print 'last iteration min h %f is from node %i' %(min_h,next_node)

    NI = Graph.GetNI(next_node)

    h_st = hue(next_node,t)

    print 'this iteration h_st %f is from node %i' %(h_st,next_node)

    for Id in NI.GetOutEdges():


        print "outward connected node %d" % (Id)

        if Id == t:
          print 'found target node after %i steps' %(steps)
          return True,steps

        else:
          h = hue(Id, t)

        if h < min_h:
          min_h = h
          next_node = Id

    steps += 1

    print '%i steps passed' %(steps)


  ############################################################################
  print 'did not found target node '
  return False, -1


def edgeProbability(alpha, v, w):
  """
  :param - alpha: given parameter [refer to 3.3]
  :param - v: node id
  :param - w: node id

  return type: Int
  return: p_v(w) [refer to 3.2]
  """
  return (b ** (-(alpha * hue(v,w))))


def Z(alpha):
  """
  :param - alpha: given parameter [refer to 3.3]

  return type: Float
  return: Normalizing constant [refer to 3.2]
  """
  z = 0.0
  for i in range(1, hT+1):
    z += (pow(b, i) - pow(b, i-1)) * pow(b, -i * alpha);

  return z


def createEdges(Graph, alpha):
  """
  :param - Graph: snap.TNGraph object representing a directed graph
  :param - alpha: given parameter [refer to 3.3]

  return type: snap.TNGraph
  return: A directed graph with edges constructed according to description
  [refer to 3.2]
  """
  ############################################################################
  # TODO: Your code here! (Hint: use Graph.AddEdge() to add edges)
  # for each node, sample as many times until it has k==5 out edges
  num_edges = 0

  total_nodes = Graph.GetNodes()

  h = {}

  for n1 in range(total_nodes):

    print 'now working on source node ', n1

    node_choices = range(total_nodes)

    if n1 in h.keys():

      exit_connections = h[n1]

      node_choices =  [n for n in node_choices if n not in exit_connections]

    h_choices = [edgeProbability(alpha, n1, x) for x in node_choices]
    Z = np.sum(h_choices)
    print 'self calculated Z is', Z

    prob_choices = [float(x)/Z for x in h_choices]

    NI = Graph.GetNI(n1)

    while NI.GetOutDeg() < 5:

      n2 = np.random.choice(node_choices, p=prob_choices)

      Graph.AddEdge(n1,n2)

      print 'connect %i with %i now' %(n1,n2)

      # Add connection edge to n1 key

      if n1 in h.keys():

        h[n1].append(n2)

      else:
        h[n1] = [n2]

      # Add connection edge to n2 key
      if n2 in h.keys():

        h[n2].append(n1)

      else:
        h[n2] = [n1]

      # Get the index of n2 from nodes_choice
      idx = node_choices.index(n2)
      # remove n2 from nodes_choice
      del node_choices[idx]
      # remove n2's probability from prob_choice
      del h_choices[idx]
      # recompute Z
      Z = np.sum(h_choices)
      # update prob choices
      prob_choices = [float(x)/Z for x in h_choices]

    assert NI.GetOutDeg() == 5

  print 'edge creation finished'

  return Graph


  ############################################################################


def runExperiment(alpha):
  """
  :param - alpha: given parameter [refer to 3.3]

  return type: [float, float]
  return: [average path length, success probability]
  """

  Graph = snap.TNGraph.New()
  for i in range(0, b ** 10):
    Graph.AddNode(i)

  Graph = createEdges(Graph, alpha)
  nodes = sampleNodes()

  c_success = 0.0
  c_path = 0.0

  for i in range(0, 1000):
    found, path = search(Graph, nodes[i][0], nodes[i][1])
    if found:
      c_success += 1
      c_path += path

  p_success = c_success/1000.0
  a_path = -1

  if c_success != 0:
    a_path = c_path/c_success

  return [a_path, p_success]

def main():
  results = []
  alpha = 0.1

  while (alpha <= 10):
    results.append([alpha] + runExperiment(alpha))
    alpha += 0.1
    print ' '.join(map(str, results[-1]))

  plt.figure(1);
  plt.plot([data[0] for data in results], [data[1] for data in results], marker='o', markersize=3)
  plt.xlabel('Parameter alpha')
  plt.ylabel('Average Path Length')
  plt.title('Average Path Length vs alpha')

  plt.figure(2);
  plt.plot([data[0] for data in results], [data[2] for data in results], marker='o', markersize=3)
  plt.xlabel('Parameter alpha')
  plt.ylabel('Success Rate')
  plt.title('Success Rate vs alpha')

  plt.show()


if __name__ == "__main__":
    main()