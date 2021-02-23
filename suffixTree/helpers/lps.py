from .base import Base


class LPS(Base):
	"""Longest Palindromic Substring"""

	def __init__(self, tree, k):
		super(LPS, self).__init__(tree)
		self.maxHeight = 0
		self.substringStartIndex = 0
		self.numberOfInternalNodes = 0

	def doTraversal(self,
					node,
					labelHeight):

		if node is None:
			return

		if not node.leaf:
			for child in node.children.values():
				self.doTraversal(child, labelHeight + child.edge_length())
				if self.maxHeight < labelHeight and len(node.forwardIndices) > 0 and len(node.reverseIndices) > 0:
					for forwardIndex in node.forwardIndices:
						reverseIndex = (len(
							self.tree.strings[0]) - 2) - (forwardIndex + labelHeight - 1)
						if reverseIndex in node.reverseIndices:
							self.maxHeight = labelHeight
							self.substringStartIndex = node.end - labelHeight + 1
							break

	def find(self):
		self.maxHeight = 0
		self.substringStartIndex = 0
		self.doTraversal(self.root, 0)
		if self.maxHeight:
			return self.string[self.substringStartIndex: self.substringStartIndex + self.maxHeight]
		else:
			return -1
