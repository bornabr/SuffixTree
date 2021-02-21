from .base import Base


class LCS(Base):
	"""Longest Common Substring"""

	def __init__(self, tree, k):
		super(LCS, self).__init__(tree)
		self.stringsRange = []
		index = 0
		for string in self.tree.strings:
			length = len(string)
			self.stringsRange.append((index, index + length - 2))
			index += length
		self.k = k
		self.maxHeight = 0
		self.subStringStartIndex = 0
		self.numberOfInternalNodes = 0

	def doTraversal(self,
					node,
					labelHeight):

		if node is None:
			return set([])
		if not node.leaf:
			# strings that this node path to its leaf generate are suffix of which of the first strings of this tree
			node.strings = set([])
			for child in node.children.values():
				res = self.doTraversal(child, labelHeight + child.edge_length())
				node.strings = node.strings.union(res)
			if len(node.strings) >= self.k and self.maxHeight < labelHeight:
				self.maxHeight = labelHeight
				self.substringStartIndex = node.end - labelHeight + 1
			return node.strings
		else:
			for index, (start, end) in enumerate(self.stringsRange):
				if start <= node.suffixIndex <= end:
					node.strings = set([index])
					return node.strings
			return set([])
					

	def find(self):
		self.maxHeight = 0
		self.substringStartIndex = 0
		res = self.doTraversal(self.root, 0)
		if self.maxHeight:
			return self.string[self.substringStartIndex: self.substringStartIndex + self.maxHeight]
		else:
			return -1
