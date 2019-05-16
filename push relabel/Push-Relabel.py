import numpy as np
class Edge:
	def __init__(self, flow, capacity, u, v):
	    self.flow=flow
	    self.capacity=capacity
	    self.u=u
	    self.v=v

class Node:
	def __init__(self, h, e_flow):
	    self.h=h
	    self.e_flow=e_flow


class Graph:
	def __init__(self, V):
	    self.V=V
	    self.Ver=[]
	    self.edge=[]
	    for i in range(V):
	        self.Ver.append(Node(0,0))

	def addEdge(self, u, v, cap):
	    self.edge.append(Edge(0, cap, u, v))

	def preFlow(self, s):
	    self.Ver[s].h = len(self.Ver)
	    for i in range(len(self.edge)):
	        if self.edge[i].u ==s:
	            self.edge[i].flow = self.edge[i].capacity
	            self.Ver[self.edge[i].v].e_flow += self.edge[i].flow
	            self.edge.append(Edge(-self.edge[i].flow, 0, self.edge[i].v, s))

	def overflowNode(self):
	    for i in range(1,len(self.Ver)-1):
	        if self.Ver[i].e_flow > 0:
	            return i  
	    return -1

	def updateReverseEdgeFlow(self, i, flow):
	    u = self.edge[i].v
	    v = self.edge[i].u
	    
	    for j in range(len(self.edge)):
	        if self.edge[j].v==v and self.edge[j].u==u:
	            self.edge[j].flow -= flow
	            return
	        
	    self.edge.append(Edge(0, flow, u, v))

	def push(self, u):
	    for i in range(len(self.edge)):
	        if self.edge[i].u == u:
	            if self.edge[i].flow == self.edge[i].capacity:
	                continue
	            if self.Ver[u].h > self.Ver[self.edge[i].v].h:
	                flow = np.minimum(self.edge[i].capacity - self.edge[i].flow, self.Ver[u].e_flow)
	                self.Ver[u].e_flow -= flow
	                self.Ver[self.edge[i].v].e_flow += flow
	                self.edge[i].flow += flow
	                self.updateReverseEdgeFlow(i, flow)
	                return True
	    return False

	def relabel(self, u):
	    mh = np.inf
	    for i in range(len(self.edge)):
	        if self.edge[i].u == u:
	            if self.edge[i].flow == self.edge[i].capacity:
	                continue
	            if self.Ver[self.edge[i].v].h < mh:
	                mh = self.Ver[self.edge[i].v].h
	                self.Ver[u].h = mh+1

	def getMaxFlow(self, s, t):
	    self.preFlow(s)
	    while self.overflowNode() != -1:
	        u = self.overflowNode()
	        if not self.push(u):
	            self.relabel(u)
	    return self.Ver[-1].e_flow

g = Graph(6)
    
g.addEdge(0, 1, 16)
g.addEdge(0, 2, 13)
g.addEdge(1, 2, 10)
g.addEdge(2, 1, 4)
g.addEdge(1, 3, 12)
g.addEdge(2, 4, 14)
g.addEdge(3, 2, 9)
g.addEdge(3, 5, 20)
g.addEdge(4, 3, 7)
g.addEdge(4, 5, 4)

s = 0
t = 5
print(g.getMaxFlow(s,t))
