from Tree import Tree
from LogicTree import LogicTree
from HeavyLight import HeavyLight

t = Tree(1)
t.add(1, 2, True)
t.add(1, 3, True)
t.add(2, 4, False)
t.add(2, 5, True)
t.add(3, 6, False)
t.add(3, 7, True)
t.add(5, 8, False)
t.add(5, 9, True)


lt = LogicTree(t) # precondicionamiento O(n), consultas O(log n) promedio, O(n) peor caso

hl = HeavyLight(t) # precondicionamiento O(n), consultas O(log n)


# Consultas de forall
assert lt.forall(1, 9) == hl.forall(1, 9) == True
assert lt.forall(1, 8) == hl.forall(1, 8) == False
assert lt.forall(1, 3) == hl.forall(1, 3) == True
assert lt.forall(1, 6) == hl.forall(1, 6) == False
assert lt.forall(2, 5) == hl.forall(2, 5) == True
assert lt.forall(2, 8) == hl.forall(2, 8) == False
assert lt.forall(2, 3) == hl.forall(2, 3) == True
assert lt.forall(8, 7) == hl.forall(8, 7) == False
assert lt.forall(9, 6) == hl.forall(9, 6) == False
assert lt.forall(9, 7) == hl.forall(9, 7) == True
assert lt.forall(7, 9) == hl.forall(7, 9) == True
assert lt.forall(1, 1) == hl.forall(1, 1) == True

# Consultas de exists
assert lt.exists(1, 9) == hl.exists(1, 9) == True
assert lt.exists(1, 8) == hl.exists(1, 8) == True
assert lt.exists(1, 3) == hl.exists(1, 3) == True
assert lt.exists(1, 6) == hl.exists(1, 6) == True
assert lt.exists(2, 5) == hl.exists(2, 5) == True
assert lt.exists(2, 8) == hl.exists(2, 8) == True
assert lt.exists(2, 3) == hl.exists(2, 3) == True
assert lt.exists(8, 7) == hl.exists(8, 7) == True
assert lt.exists(9, 6) == hl.exists(9, 6) == True
assert lt.exists(9, 7) == hl.exists(9, 7) == True
assert lt.exists(7, 9) == hl.exists(7, 9) == True
assert lt.exists(1, 1) == hl.exists(1, 1) == False
assert lt.exists(2, 4) == hl.exists(2, 4) == False
assert lt.exists(5, 8) == hl.exists(5, 8) == False
assert lt.exists(3, 6) == hl.exists(3, 6) == False

lt.tree.costs[(1, 2)] = hl.tree.costs[(1, 2)] = False
lt.tree.costs[(2, 1)] = hl.tree.costs[(2, 1)] = False
lt.tree.costs[(2, 5)] = hl.tree.costs[(2, 5)] = False
lt.tree.costs[(1, 3)] = hl.tree.costs[(1, 3)] = False

assert lt.forall(1, 8) == hl.forall(1, 8) == False
assert lt.forall(1, 6) == hl.forall(1, 6) == False
assert lt.forall(8, 6) == hl.forall(8, 6) == False