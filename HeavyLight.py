from Tree import Tree
from LCA import LCA

class HeavyLight:
	def __init__(self, tree):
		self.tree = tree
		self.n = len(tree.nodes)
		self.size = {}
		self.depth = {}
		self.chainID = {}
		self.chainList = []
		self.forallST = []
		self.existsST = []

		self.dfs(tree.root.key)
		self.hld(tree.root.key)
		self.lca = LCA(tree)

		for chain in self.chainList:
			self.forallST.append(self.ForallST(chain))
			self.existsST.append(self.ExistsST(chain))

	def forall(self, x, y):
		chainX = self.chainID[x]
		chainY = self.chainID[y]

		# si los nodos están en la misma cadena, se hace la consulta en el arbol de segmentos
		if chainX == chainY:
			return self.forallST[chainX].query(x, y)

		# si no, se busca el ancestro común y se evalua la consulta para cada cadena
		ancestor = self.lca.query(x, y)
		return self.crawl_forall(x, ancestor) and self.crawl_forall(y, ancestor)
	
	def crawl_forall(self, x, ancestor):
		chainAncestor = self.chainID[ancestor]
		
		res = True

		# se recorre la cadena del nodo hasta llegar al ancestro
		while True:
			chainX = self.chainID[x]
			
			# si se llega a la cadena del ancestro, se evalua el nodo y se termina
			if chainX == chainAncestor:
				if x != ancestor:
					res = res and self.forallST[chainX].query(x, ancestor)
				break
			
			# si no, se evalua el nodo hasta la raiz de su cadena y se avanza al padre de la raiz
			else:
				res = res and self.forallST[chainX].query(x, self.chainList[chainX][0].key)
				res = res and self.chainList[chainX][0].cost
				x = self.chainList[chainX][0].parent.key

		return res
	
	def exists(self, x, y):
		chainX = self.chainID[x]
		chainY = self.chainID[y]

		# si los nodos están en la misma cadena, se hace la consulta en el arbol de segmentos
		if chainX == chainY:
			return self.existsST[chainX].query(x, y)

		# si no, se busca el ancestro común y se evalua la consulta para cada cadena
		ancestor = self.lca.query(x, y)
		return self.crawl_exists(x, ancestor) or self.crawl_exists(y, ancestor)
	
	def crawl_exists(self, x, ancestor):
		chainAncestor = self.chainID[ancestor]
		
		res = False

		# se recorre la cadena del nodo hasta llegar al ancestro
		while True:
			chainX = self.chainID[x]
			
			# si se llega a la cadena del ancestro, se evalua el nodo y se termina
			if chainX == chainAncestor:
				if x != ancestor:
					res = res or self.existsST[chainX].query(x, ancestor)
				break
			
			# si no, se evalua el nodo hasta la raiz de su cadena y se avanza al padre de la raiz
			else:
				res = res or self.existsST[chainX].query(x, self.chainList[chainX][0].key)
				res = res or self.chainList[chainX][0].cost
				x = self.chainList[chainX][0].parent.key

		return res

	def dfs(self, vertex, depth=0):
		self.depth[vertex] = depth
		self.size[vertex] = 1

		for child in self.tree.children(vertex):
			self.size[vertex] += self.dfs(child.key, depth + 1)

		return self.size[vertex]
	
	def hld(self, vertex, chainID=None):
		# si no se especifica la cadena, se crea una nueva
		if chainID is None:
			chainID = len(self.chainList)
			self.chainList.append([])

		# se asigna el nodo a la cadena y se guarda la cadena del nodo
		self.chainID[vertex] = chainID
		newNode = self.tree.nodes[vertex]
		if len(self.chainList[chainID]) > 0 and newNode.parent != self.chainList[chainID][-1]:
			raise ValueError(f"El nodo {newNode} no es hijo del último nodo de la cadena {self.chainList[chainID]}")
		self.chainList[chainID].append(newNode)

		# se busca el hijo con mayor tamaño
		heaviest = None
		for child in self.tree.children(vertex):
			if heaviest is None or self.size[child.key] > self.size[heaviest]:
				heaviest = child.key

		# si hay un hijo con mayor tamaño, se le asigna la misma cadena
		if heaviest is not None:
			self.hld(heaviest, chainID)

		# se asignan las demás cadenas a los demás hijos
		for child in self.tree.children(vertex):
			if child.key != heaviest:
				self.hld(child.key)

	def chain(self, node):
		return self.chainList[self.chainID[node]]
	
	class ForallST:
		def __init__(self, arr):
			costs = [node.cost for node in arr[1:]]
			self.index = {node.key: i for i, node in enumerate(arr)}
			self.n = len(costs)
			self.tree = [True] * (2 * self.n)
			self.tree[self.n:] = costs

			for i in range(self.n - 1, 0, -1):
				self.tree[i] = self.tree[i << 1] and self.tree[i << 1 | 1]

		def query(self, x, y):
			# se busca el índice de los nodos y se ordenan
			l = self.index[x]
			r = self.index[y]
			if l > r:
				l, r = r, l

			l += self.n
			r += self.n
			res = True

			while l < r:
				if l & 1:
					res = res and self.tree[l]
					l += 1

				if r & 1:
					r -= 1
					res = res and self.tree[r]

				l >>= 1
				r >>= 1

			return res
		
	class ExistsST:
		def __init__(self, arr):
			costs = [node.cost for node in arr[1:]]
			self.index = {node.key: i for i, node in enumerate(arr)}
			self.n = len(costs)
			self.tree = [0 for _ in range(2 * self.n)]
			self.tree[self.n:] = costs

			for i in range(self.n - 1, 0, -1):
				self.tree[i] = self.tree[i << 1] or self.tree[i << 1 | 1]

		def query(self, x, y):
			# se busca el índice de los nodos y se ordenan
			l = self.index[x]
			r = self.index[y]
			if l > r:
				l, r = r, l

			l += self.n
			r += self.n
			res = False

			while l < r:
				if l & 1:
					res = res or self.tree[l]
					l += 1

				if r & 1:
					r -= 1
					res = res or self.tree[r]

				l >>= 1
				r >>= 1

			return res
		
if __name__ == "__main__":
	t = Tree(1)
	t.add(1, 2, True)
	t.add(1, 3, True)
	t.add(2, 4, False)
	t.add(2, 5, True)
	t.add(3, 6, False)
	t.add(3, 7, True)
	t.add(5, 8, False)
	t.add(5, 9, True)
	hl = HeavyLight(t)

	assert hl.forall(1, 9) == True
	assert hl.forall(1, 8) == False
	assert hl.forall(1, 3) == True
	assert hl.forall(1, 6) == False
	assert hl.forall(2, 5) == True
	assert hl.forall(2, 8) == False
	assert hl.forall(2, 3) == True
	assert hl.forall(2, 4) == False
	assert hl.forall(8, 7) == False
	assert hl.forall(9, 6) == False
	assert hl.forall(9, 7) == True
	assert hl.forall(7, 9) == True
	assert hl.forall(1, 1) == True

	assert hl.exists(1, 9) == True
	assert hl.exists(1, 8) == True
	assert hl.exists(1, 3) == True
	assert hl.exists(1, 6) == True
	assert hl.exists(2, 5) == True
	assert hl.exists(2, 8) == True
	assert hl.exists(2, 3) == True
	assert hl.exists(8, 7) == True
	assert hl.exists(9, 6) == True
	assert hl.exists(9, 7) == True
	assert hl.exists(7, 9) == True
	assert hl.exists(1, 1) == False
	assert hl.exists(2, 4) == False
	assert hl.exists(5, 8) == False
	assert hl.exists(3, 6) == False

	hl.tree.costs[(1, 2)] = False
	hl.tree.costs[(2, 1)] = False
	hl.tree.costs[(2, 5)] = False
	hl.tree.costs[(1, 3)] = False

	assert hl.forall(1, 8) == False
	assert hl.forall(1, 6) == False
	assert hl.forall(8, 6 ) == False