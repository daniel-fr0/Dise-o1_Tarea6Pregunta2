class Node:
	def __init__(self, key, parent=None, cost=None):
		self.key = key
		self.parent = parent
		self.cost = cost

	def __str__(self):
		if self.cost is None:
			return f"{self.key}"
		return f"({self.key}, {self.cost})"
	
	def __repr__(self):
		return self.__str__()

class Tree:
	def __init__(self, root):
		self.root = Node(root)
		self.tree = {root: []}
	
	def add(self, u, v, cost=None):
		if u not in self.tree:
			raise ValueError(f"Nodo de origen '{u}' no existe en el árbol")
		
		if v in self.tree:
			raise ValueError(f"Nodo de destino '{v}' ya existe en el árbol")

		self.tree[v] = []
		self.tree[u].append(Node(v, u, cost))

	def children(self, vertex):
		yield from self.tree[vertex] if vertex in self.tree else []

	def __str__(self):
		return str(self.tree)

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