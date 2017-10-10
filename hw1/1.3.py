################################################################################
# CS 224W (Fall 2017) - HW1
# Starter code for Problem 3.3
# Author: anunay@stanford.edu
# Last Updated: Sep 27, 2017
################################################################################

import snap
import sys
import math
import random


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


def h(v, w):
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

  ############################################################################

  return False, -1


def edgeProbability(alpha, v, w):
  """
  :param - alpha: given parameter [refer to 3.3]
  :param - v: node id
  :param - w: node id

  return type: Int
  return: p_v(w) [refer to 3.2]
  """
  return (b ** (-(alpha * h(v,w))))


def Z(Graph, alpha):
  """
  :param - Graph: snap.TNGraph object representing a directed graph
  :param - alpha: given parameter [refer to 3.3]

  return type: Float
  return: Normalizing constant [refer to 3.2]
  """
  z = 0.0
  for i in range(0, b ** hT):
    for j in range(0, b ** hT):
      z += edgeProbability(alpha, i, j)
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

  ############################################################################

  return Graph


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

  for res in results:
    print ' '.join(map(str, res))

if __name__ == "__main__":
    main()