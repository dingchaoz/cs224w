import snap
import numpy as np
import matplotlib.pyplot as plt

'''
Problem 2
'''

Gwiki = snap.LoadEdgeList(snap.PNGraph,'wiki-Vote.txt',0,1)

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
plt.xlim([0, max(logY)])
plt.plot(logX,logY)


'''
2.2
Compute and plot least-square regression line
Use numpy polyfit with deg == 1
'''
idx = np.isfinite(logX) & np.isfinite(logY)
coefficients = np.polyfit(logX[idx], logY[idx], 1)
polynomial = np.poly1d(coefficients)
ys = polynomial(logX)
plt.plot(logX, ys)
print 'a is %f and b is %f' % (coefficients[0],coefficients[1])
