# Code based on the implementation of Heavy Light Decomposition from GeeksForGeeks
# https://www.geeksforgeeks.org/implementation-of-heavy-light-decomposition/

N = 1024

# Matrix representing the tree
tree = [[-1 for _ in range(N)] for _ in range(N)]

class Node:
	def __init__(self):
		self.parent = None  # Parent of this node
		self.depth = None  # Depth of this node
		self.size = None  # Size of subtree rooted with this node
		self.segment_base_position = None  # Position in segment tree base
		self.chain = None

# Initialize nodes
nodes = [Node() for _ in range(N)]

class Edge:
	def __init__(self):
		self.weight = None  # Weight of Edge
		self.deeper_end = None  # Deeper end

# Initialize edges
edges = [Edge() for _ in range(N)]

class SegmentTree:
	def __init__(self):
		self.base_array = [0 for _ in range(N)]
		self.tree = [0 for _ in range(6 * N)]

# Initialize segment tree
segment_tree = SegmentTree()

# Function to add edges to the tree
def add_edge(edge_id, u, v, weight):
	tree[u - 1][v - 1] = edge_id - 1
	tree[v - 1][u - 1] = edge_id - 1
	edges[edge_id - 1].weight = weight

# Recursive function for DFS on the tree
def dfs(current_node, previous_node, depth, n):
	nodes[current_node].parent = previous_node
	nodes[current_node].depth = depth
	nodes[current_node].size = 1

	for j in range(n):
		if j != current_node and j != nodes[current_node].parent and tree[current_node][j] != -1:
			edges[tree[current_node][j]].deeper_end = j
			dfs(j, current_node, depth + 1, n)
			nodes[current_node].size += nodes[j].size

# Recursive function that decomposes the Tree into chains
def hld(current_node, edge_count, edge_counted, current_chain, n, chain_heads):
	if chain_heads[current_chain[0]] == -1:
		chain_heads[current_chain[0]] = current_node

	nodes[current_node].chain = current_chain[0]
	nodes[current_node].segment_base_position = edge_counted[0]
	segment_tree.base_array[edge_counted[0]] = edges[edge_count].weight
	edge_counted[0] += 1

	special_child = -1
	special_edge_id = None
	for j in range(n):
		if j != current_node and j != nodes[current_node].parent and tree[current_node][j] != -1:
			if special_child == -1 or nodes[special_child].size < nodes[j].size:
				special_child = j
				special_edge_id = tree[current_node][j]

	if special_child != -1:
		hld(special_child, special_edge_id, edge_counted, current_chain, n, chain_heads)

	for j in range(n):
		if j != current_node and j != nodes[current_node].parent and j != special_child and tree[current_node][j] != -1:
			current_chain[0] += 1
			hld(j, tree[current_node][j], edge_counted, current_chain, n, chain_heads)

# Recursive function that constructs Segment Tree for array[ss..se)
def construct_segment_tree(ss, se, si):
	if ss == se - 1:
		segment_tree.tree[si] = segment_tree.base_array[ss]
		return segment_tree.base_array[ss]

	mid = (ss + se) // 2
	segment_tree.tree[si] = max(construct_segment_tree(ss, mid, si * 2), construct_segment_tree(mid, se, si * 2 + 1))
	return segment_tree.tree[si]

# Recursive function that updates the Segment Tree
def update_segment_tree(ss, se, si, x, val):
	if ss > x or se <= x:
		return segment_tree.tree[si]

	elif ss == x and ss == se - 1:
		segment_tree.tree[si] = val
		return val

	else:
		mid = (ss + se) // 2
		segment_tree.tree[si] = max(update_segment_tree(ss, mid, si * 2, x, val),
									update_segment_tree(mid, se, si * 2 + 1, x, val))
		return segment_tree.tree[si]

# Function to update Edge's value to val in segment tree
def change_edge_value(edge_id, value, n):
	update_segment_tree(0, n, 1, nodes[edges[edge_id].deeper_end].segment_base_position, value)

# Function to get the LCA of nodes u and v
def lowest_common_ancestor(u, v, n):
	lca_aux = [-1 for _ in range(n + 5)]

	if nodes[u].depth < nodes[v].depth:
		u, v = v, u

	while u != -1:
		lca_aux[u] = 1
		u = nodes[u].parent

	while v:
		if lca_aux[v] == 1:
			break
		v = nodes[v].parent

	return v

# Recursive function to get the maximum value in a given range of array indexes
def range_maximum_query_util(ss, se, qs, qe, index):
	if qs <= ss and qe >= se - 1:
		return segment_tree.tree[index]

	if se - 1 < qs or ss > qe:
		return -1

	mid = (ss + se) // 2
	return max(range_maximum_query_util(ss, mid, qs, qe, 2 * index),
			   range_maximum_query_util(mid, se, qs, qe, 2 * index + 1))

# Return maximum of elements in range from index qs (query start) to qe (query end)
def range_maximum_query(qs, qe, n):
	if qs < 0 or qe > n - 1 or qs > qe:
		print("Invalid Input")
		return -1

	return range_maximum_query_util(0, n, qs, qe, 1)

# Function to move from u to v keeping track of the maximum
def crawl_tree(u, v, n, chain_heads):
	chain_v = nodes[v].chain
	ans = 0

	while True:
		chain_u = nodes[u].chain

		if chain_u == chain_v:
			if u != v:
				ans = max(range_maximum_query(nodes[v].segment_base_position + 1, nodes[u].segment_base_position, n), ans)
			break

		else:
			ans = max(ans, range_maximum_query(nodes[chain_heads[chain_u]].segment_base_position,
											   nodes[u].segment_base_position, n))
			u = nodes[chain_heads[chain_u]].parent

	return ans

# Function for MAX_EDGE query
def max_edge_query(u, v, n, chain_heads):
	lca = lowest_common_ancestor(u, v, n)
	ans = max(crawl_tree(u, lca, n, chain_heads), crawl_tree(v, lca, n, chain_heads))
	print(f"Max edge between {u} and {v} is {ans}")

def main():
	n = 11

	add_edge(1, 1, 2, 13)
	add_edge(2, 1, 3, 9)
	add_edge(3, 1, 4, 23)
	add_edge(4, 2, 5, 4)
	add_edge(5, 2, 6, 25)
	add_edge(6, 3, 7, 29)
	add_edge(7, 6, 8, 5)
	add_edge(8, 7, 9, 30)
	add_edge(9, 8, 10, 1)
	add_edge(10, 8, 11, 6)

	root = 0
	parent_of_root = -1
	depth_of_root = 0

	dfs(root, parent_of_root, depth_of_root, n)

	chain_heads = [-1 for _ in range(N)]

	edge_counted = [0]
	current_chain = [0]

	hld(root, n - 1, edge_counted, current_chain, n, chain_heads)

	construct_segment_tree(0, edge_counted[0], 1)

	u = 11
	v = 9
	print(f"Max edge between {u} and {v} is ", end="")
	max_edge_query(u - 1, v - 1, n, chain_heads)

	change_edge_value(8 - 1, 28, n)

	print(f"After Change: max edge between {u} and {v} is ", end="")
	max_edge_query(u - 1, v - 1, n, chain_heads)

	v = 4
	print(f"Max edge between {u} and {v} is ", end="")
	max_edge_query(u - 1, v - 1, n, chain_heads)

	change_edge_value(5 - 1, 22, n)
	print(f"After Change: max edge between {u} and {v} is ", end="")
	max_edge_query(u - 1, v - 1, n, chain_heads)

if __name__ == "__main__":
	main()