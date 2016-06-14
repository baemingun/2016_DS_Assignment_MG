import os

class Node:
	def __init__(self):
		self.p = None
		self.left = None
		self.right = None

class RBTNode(Node):
	def __init__(self):
		super().__init__()
		self.red = False
		self.key = None

	def make_node(self,key):
		n = RBTNode()
		n.key = key
		return n

class RBTree:
	def __init__(self):
		self.root = None
		self.nil = None
	
	def insert(self,z):
		y = self.nil
		x = self.root
		while x != self.nil:
			y = x
			if x.key != None and  z.key < x.key:
				x = x.left
			else:
				x = x.right
		z.p = y
		if y == self.nil:
			self.root = z
		elif z.key < y.key:
			y.left = z
		else:
			y.right = z
		z.left = self.nil
		z.right = self.nil
		z.red = True
		self.fixup(z)

	def fixup(self,z):
		while z.p.red == True:
			if z.p == z.p.p.left:
				y = z.p.p.right
				if y.red == True:
					z.p.red = False
					y.red = False
					z.p.p.red = True
					z = z.p.p
				else:
					if z == z.p.right:
						z = z.p
						self.left_rotate(z)
					z.p.red = False
					z.p.p.red = True
					self.right_rotate(z.p.p)
			else:
				y = z.p.p.left
				if y.red == True:
					z.p.red = False
					y.red = False
					z.p.p.red = True
					z = z.p.p
				else:
					if z == z.p.left:
						z = z.p
						self.right_rotate(z)
					z.p._red = False
					z.p.p._red = True
					self.left_rotate(z.p.p)
		self.root.red = False

	def left_rotate(self, z):
		x = z.right
		z.right = x.left
		if x.left != self.nil:
			x.left._p = z
		x.p = z.p
		if z.p == self.nil:
			self.root = x
		elif z == z.p.left:
			z.p.left = x
		else:
			z.p.right = x
		x.left = z
		z.p = x

	def right_rotate(self, z):
		x = z.left
		z.left = x.right
		if x.right != self.nil:
			x.right.p = z
		x.p = z.p
		if z.p == self.nil:
			self.root = x
		elif z == z.p.right:
			z.p.right = x
		else:
			z.p._left = x
		x.right = z
		z.p = x

	def print_util(self, tree, level):
		if (tree.right):
			self.print_util(tree.right, level + 1)
		for i in range(level):
			print('    ', end = '')
		tree.print_node()
		if (tree.left):
			self.print_util(tree.left, level + 1)
	def print_tree(self):
		self.print_util(self.root, 0)


def menu():
	print("0. Read data files")
	print("1. display statistics")
	print("2. Top 5 most tweeted words")
	print("3. Top 5 most tweeted users")
	print("4. Find users who tweeted a word (e.g., ’연세대’)")
	print("5. Find all people who are friends of the above users")
	print("6. Delete users who mentioned a word")
	print("7. Delete all users who mentioned a word")
	print("8. Find strongly connected components")
	print("9. Find shortest path from a given user")
	print("99. Quit")
	return int(input("Select Menu: "))

def main():
	while(1):
		os.system("cls")
		rb = RBTNode()
		a = RBTree()
		a.root = rb. make_node(1)
		a.insert(rb.make_node(2))
		a.print_tree()
		a.insert(rb.make_node(3))
		a.insert(rb.make_node(4))
		a.insert(rb.make_node(5))
		a.print_tree()
		num = menu()
		if(num == 0):
			pass
		elif(num == 1):
			pass
		elif(num == 2):
			pass
		elif(num == 3):
			pass
		elif(num == 4):
			pass
		elif(num == 5):
			pass
		elif(num == 6):
			pass
		elif(num == 7):
			pass
		elif(num == 8):
			pass
		elif(num == 9):
			pass
		elif(num == 99):
			break
		os.system("pause")


main()