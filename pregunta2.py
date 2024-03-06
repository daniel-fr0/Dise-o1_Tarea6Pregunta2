from Tree import Tree
from LCA import LCA

class LogicTree():
	def __init__(self, tree):
		self.tree = tree
		# O(n) en tiempo y espacio, cada consulta toma O(log n)
		self.lca = LCA(tree)


	# consulta el camino entre x y y, O(log n) si el arbol es balanceado
	# O(n) en el peor caso si el arbol es una lista
	def forall(self, x, y):
		if x == y:
			return True
		
		ancestor = self.lca.query(x, y)

		start = x if ancestor == y else y if ancestor == x else None

		if start:
			parent = self.tree.nodes[start].parent.key
			return self.tree.p(start, parent) and self.forall(parent, ancestor)

		parentX = self.tree.nodes[x].parent.key
		parentY = self.tree.nodes[y].parent.key
		return (
			self.tree.p(x, parentX) and self.forall(parentX, ancestor)
			and
			self.tree.p(y, parentY) and self.forall(parentY, ancestor)
		)

	# consulta el camino entre x y y, O(log n) si el arbol es balanceado
	# O(n) en el peor caso si el arbol es una lista
	def exists(self, x, y):
		if x == y:
			return False
		
		ancestor = self.lca.query(x, y)

		start = x if ancestor == y else y if ancestor == x else None

		if start:
			parent = self.tree.nodes[start].parent.key
			return self.tree.p(start, parent) or self.exists(parent, ancestor)

		parentX = self.tree.nodes[x].parent.key
		parentY = self.tree.nodes[y].parent.key
		return (
			self.tree.p(x, parentX) or self.exists(parentX, ancestor)
			or
			self.tree.p(y, parentY) or self.exists(parentY, ancestor)
		)


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
	lt = LogicTree(t)

	assert lt.forall(1, 9) == True
	assert lt.forall(1, 8) == False
	assert lt.forall(1, 3) == True
	assert lt.forall(1, 6) == False
	assert lt.forall(2, 5) == True
	assert lt.forall(2, 8) == False
	assert lt.forall(2, 3) == True
	assert lt.forall(8, 7) == False
	assert lt.forall(9, 6) == False
	assert lt.forall(9, 7) == True
	assert lt.forall(7, 9) == True
	assert lt.forall(1, 1) == True

	assert lt.exists(1, 9) == True
	assert lt.exists(1, 8) == True
	assert lt.exists(1, 3) == True
	assert lt.exists(1, 6) == True
	assert lt.exists(2, 5) == True
	assert lt.exists(2, 8) == True
	assert lt.exists(2, 3) == True
	assert lt.exists(8, 7) == True
	assert lt.exists(9, 6) == True
	assert lt.exists(9, 7) == True
	assert lt.exists(7, 9) == True
	assert lt.exists(1, 1) == False
	assert lt.exists(2, 4) == False
	assert lt.exists(5, 8) == False
	assert lt.exists(3, 6) == False

	lt.tree.costs[(1, 2)] = False
	lt.tree.costs[(2, 1)] = False
	lt.tree.costs[(2, 5)] = False
	lt.tree.costs[(1, 3)] = False

	assert lt.forall(1, 8) == False
	assert lt.forall(1, 6) == False
	assert lt.forall(8, 6 ) == False