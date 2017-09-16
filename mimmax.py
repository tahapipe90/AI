from networkx import DiGraph


class Minimax():

	def __init__(self, graph):
		self.graph = graph
		self.depthMatrix = self.createDepthMatrix()
		self.closedList = []

	def minimax(self, currentDepth):
		currentBreathNodes = self.depthMatrix[
			currentDepth - 1]  # depth[length-2]

		func = self.maximize if currentDepth % 2 else self.minimize

		t = []
		for i in currentBreathNodes:
			index, value = func(self.graph[i])
			t.append(index)
			parent = self.graph.predecessors(i)
			if parent:
				self.graph[parent[0]][i]['weight'] = value
				value = None
			else:
				break

		self.closedList.append(t)

		return value

	def minimize(self, children):
		keys = children.keys()
		index = keys.pop()
		minimum = children[index]['weight']
		for i in keys:
			if minimum > children[i]['weight']:
				minimum = children[i]['weight']
				index = i

		return (index, minimum)

	def maximize(self, children):
		keys = children.keys()
		index = keys.pop()
		maximum = children[index]['weight']
		for i in keys:
			if maximum < children[i]['weight']:
				maximum = children[i]['weight']
				index = i

		return (index, maximum)

	def createDepthMatrix(self):
		depthMatrix = [[1]]
		child = [1]

		while True:
			t = []
			for node in child:
				t.extend(self.graph[node].keys())

			if not t:
				break

			depthMatrix.append(t)
			child = t

		return depthMatrix

	def findPath(self):
		path = [1]
		close = self.closedList.pop()[0]
		path.append(close)
		j = 0
		while j < len(self.depthMatrix) - 2:
			child = self.graph[close].keys()
			close_list = self.closedList.pop()
			close = [i for i in child if i in close_list].pop()
			path.append(close)
			j += 1

		return path


def main():
	n = input("Enter number of nodes : ")

	# commands
	edges = []
	N = None
	nodes = range(1, n + 1)

	print "Nodes created : ", nodes
	print "\n-> Enter edges using below syntax\n-> Enter 'N' if cost is unknown\n-> Enter 'end' with quote to continue"
	print "-> Enter 'nodes' to print all nodes\n-> Enter 'edges' to print all edges"
	print "syntax : \n>>> parent_node_no, child_node_no, edge_cost"
	while True:
		try:
			my_input = input(">>> ")
			if isinstance(my_input, tuple):
				edges.append(my_input)
				print "Edge ", my_input, "Added"
			elif isinstance(my_input, str) and my_input.lower() == 'end':
				break
			else:
				print my_input
		except NameError as error:
			print "Invalid Command!", error
			continue

	g = DiGraph()
	g.add_nodes_from(nodes)
	g.add_weighted_edges_from(edges)

	m = Minimax(g)

	# playing ...
	depth = len(m.depthMatrix)

	for i in range(depth - 1, 0, -1):
		value = m.minimax(i)
		if i % 2:
			print "Max palyed, found maximum value nodes ", m.closedList[-1]
		else:
			print "min palyed, found minimum value nodes ", m.closedList[-1]

		if value:
			print "Game end, root node value : ", value

	print "Path : " + ' - '.join(map(str, m.findPath()))

if __name__ == '__main__':
	main()

'''
output:-
Enter number of nodes : 7
Nodes created :  [1, 2, 3, 4, 5, 6, 7]

-> Enter edges using below syntax
-> Enter 'N' if cost is unknown
-> Enter 'end' with quote to continue
-> Enter 'nodes' to print all nodes
-> Enter 'edges' to print all edges
syntax : 
>>> parent_node_no, child_node_no, edge_cost
>>> nodes
[1, 2, 3, 4, 5, 6, 7]
>>> eges
Invalid Command! name 'eges' is not defined
>>> edges
[]
>>> 1,2,N
Edge  (1, 2, None) Added
>>> 1,3,N
Edge  (1, 3, None) Added
>>> 2,4,-2
Edge  (2, 4, -2) Added
>>> 2,4,2
Edge  (2, 4, 2) Added
>>> 2,4,1
Edge  (2, 4, 1) Added
>>> 2,5,1
Edge  (2, 5, 1) Added
>>> 2,5,3
Edge  (2, 5, 3) Added
>>> 2,5,4
Edge  (2, 5, 4) Added
>>> 3,6,-1
Edge  (3, 6, -1) Added
>>> 3,6,1
Edge  (3, 6, 1) Added
>>> 3,6,0
Edge  (3, 6, 0) Added
>>> 3,7,2
Edge  (3, 7, 2) Added
>>> 3,7,5
Edge  (3, 7, 5) Added
>>> 3,7,0
Edge  (3, 7, 0) Added
>>> 'end'
min palyed, found minimum value nodes  [4, 7]
Max palyed, found maximum value nodes  [2]
Game end, root node value :  1
Path : 1 - 2 - 4

'''
