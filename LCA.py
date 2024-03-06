from Tree import Tree

class LCA:
	# teniendo en cuenta n como el número de nodos del árbol
	# el precondicionamiento toma tiempo O(n) y espacio O(n)
	def __init__(self, tree: Tree):
		# el arbol consiste en un grafo dirigido de listas de adyacencia
		self.tree = tree
		# el recorrido de euler, tiene 2n - 1 nodos, esto es O(n)
		self.walk = []
		# la primera aparición de cada nodo en el recorrido de euler, O(n)
		self.first = {}

		# se construye el recorrido de euler y el arbol de segmentos
		self.eulerWalk(tree.root.key) # tiempo O(n)
		self.st = self.SegmentTree(self.walk) # tiempo O(n) y espacio O(n)
		
	# recorrido de euler, es equivalente a un DFS, esto es O(n)
	def eulerWalk(self, nodeKey, depth=0):
		self.walk.append(nodeKey)
		self.first[nodeKey] = len(self.walk) - 1

		for child in self.tree.children(nodeKey):
			self.eulerWalk(child.key, depth + 1)
			self.walk.append(nodeKey)
	
	def query(self, u, v):
		# como la consulta es en el recorrido de euler, se busca empezar por
		# el nodo que aparece primero
		l = self.first[u]
		r = self.first[v]
		if l > r:
			l, r = r, l
		return self.st.rmq(l, r)

	class SegmentTree:
		def __init__(self, arr):
			self.n = len(arr)
			# el arbol tiene 2n - 1 nodos, se usa un arreglo de 2n, esto es O(n)
			self.tree = [0] * (2 * self.n)
			self.tree[self.n:] = arr

			# se itera sobre los nodos internos del arbol, esto es O(n)
			for i in range(self.n - 1, 0, -1):
				# se construye de abajo hacia arriba, tomando min. de los hijos
				self.tree[i] = min(self.tree[i << 1], self.tree[i << 1 | 1])

		# se hace una consulta en el arbol, esto es O(log n)
		def rmq(self, l, r):
			# se recorre desde las hojas, representa el intervalo [l, r)
			l += self.n
			r += self.n
			res = float('inf')

			# se consideran los valores mientras el intervalo no sea vacio
			while l < r:
				# si el extremo izquierdo es impar(hijo derecho), se considera 
				# el valor y se avanza al nodo a la derecha
				if l & 1:
					res = min(res, self.tree[l])
					l += 1

				# si el extremo derecho es impar(hijo derecho), se avanza al 
				# nodo a la izquierda y se considera ese valor(hijo izquierdo)
				if r & 1:
					r -= 1
					res = min(res, self.tree[r])

				# se avanza hacia el padre
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
	assert lca.query(4,9) == 2
	assert lca.query(8,9) == 5
	assert lca.query(6,7) == 3
	assert lca.query(4,5) == 2
	assert lca.query(2,5) == 2
	assert lca.query(2,3) == 1
	assert lca.query(8,7) == 1
	assert lca.query(7,8) == 1

