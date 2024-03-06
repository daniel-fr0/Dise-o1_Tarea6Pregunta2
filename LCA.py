from Tree import Tree

class LCA:
	def __init__(self, tree: Tree):
		self.tree = tree # el arbol consiste en un grafo dirigido de listas de adyacencia
		self.walk = [] # el recorrido de euler
		self.first = {}	# la primera aparición de cada nodo en el recorrido de euler
		self.eulerWalk(tree.root.key)
		self.st = self.SegmentTree(self.walk)
		
	def eulerWalk(self, nodeKey, depth=0):
		self.walk.append(nodeKey)
		self.first[nodeKey] = len(self.walk) - 1

		for child in self.tree.children(nodeKey):
			self.eulerWalk(child.key, depth + 1)
			self.walk.append(nodeKey)
	
	def query(self, u, v):
		l = self.first[u]
		r = self.first[v]
		if l > r:
			l, r = r, l
		return self.st.rmq(l, r)

	class SegmentTree:
		def __init__(self, arr):
			self.n = len(arr)
			self.tree = [0] * (2 * self.n)
			self.tree[self.n:] = arr
			for i in range(self.n - 1, 0, -1):
				self.tree[i] = min(self.tree[i << 1], self.tree[i << 1 | 1])

		def rmq(self, l, r):
			l += self.n
			r += self.n
			res = float('inf')
			while l < r:
				if l & 1:
					res = min(res, self.tree[l])
					l += 1
				if r & 1:
					r -= 1
					res = min(res, self.tree[r])
				l >>= 1
				r >>= 1
			return res


if __name__ == "__main__":
	t = Tree(1)
	t.add(1, 2)
	t.add(1, 3)
	t.add(2, 4)
	t.add(2, 5)
	t.add(3, 6)
	t.add(3, 7)
	t.add(5, 8)
	t.add(5, 9)
	print(t)
	lca = LCA(t)
	print(lca.query(4,9))
	print(lca.query(8,9))
	print(lca.query(6,7))
	print(lca.query(4,5))
	print(lca.query(2,5))
	print(lca.query(2,3))
	print(lca.query(8,7))
	print(lca.query(7,8))

