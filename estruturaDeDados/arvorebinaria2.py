# Pedro Lucas Vasques
# Exercicio 1

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


root = Node(12)
root.left = Node(4)
root.right = Node(16)
root.left.left = Node(2)
root.left.right = Node(8)
root.left.right.left = Node(6)

def pre_order(node):
    if node:
        print(node.value, end=' ')
        pre_order(node.left)
        pre_order(node.right)

def post_order(node):
    if node:
        post_order(node.left)
        post_order(node.right)
        print(node.value, end=' ')

print("Pré-ordem:")
pre_order(root)

print("\nPós-ordem:")
post_order(root)


# exercicio 2
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

values = [30, 15, 60, 10, 20, 40, 80]

root = None
for val in values:
    root = insert(root, val)

def in_order(node):
    if node:
        in_order(node.left)
        print(node.value, end=' ')
        in_order(node.right)

print("Árvore em ordem:")
in_order(root)
