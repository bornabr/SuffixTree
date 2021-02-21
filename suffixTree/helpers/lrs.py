from .base import Base


class LRS(Base):
	"""Longest Repeated Substring"""

	def __init__(self, tree, k):
		super(LRS, self).__init__(tree)
		self.k = k
		self.maxHeight = 0
		self.currentHeight = 0
		self.subStringStartIndex = 0
		self.currentSubStringStartIndex = 0
		self.numberOfInternalNodes = 0

	def doTraversal(self,
					node,
					labelHeight):

		if node is None:
			return 0
		if not node.leaf:
			count = 0
			for child in node.children.values():
				res = self.doTraversal(child, labelHeight + child.edge_length())
				if node == self.root:
					# print(childKey, res)
					if res >= self.k:
						if self.maxHeight < self.currentHeight:
							self.maxHeight = self.currentHeight
							self.subStringStartIndex = self.currentSubStringStartIndex
					self.currentHeight = 0
					self.currentSubStringStartIndex = 0
				else:
					count += res
			return count
		elif self.currentHeight < labelHeight - node.edge_length():
			# print(self.numberOfInternalNodes)
			self.numberOfInternalNodes += 1
			self.currentHeight = labelHeight - node.edge_length()
			self.currentSubStringStartIndex = node.suffixIndex
		return 1

	def find(self):
		self.maxHeight = 0
		self.substringStartIndex = 0
		self.numberOfInternalNodes = 0
		self.currentHeight = 0
		self.currentSubStringStartIndex = 0
		self.doTraversal(self.root, 0)
		if self.maxHeight:
			return self.string[self.substringStartIndex: self.substringStartIndex + self.maxHeight]
		else:
			return -1
