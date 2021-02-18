from .base import Base

class SearchPattern(Base):
	def __init__(self, tree, pattern):
		super(SearchPattern, self).__init__(tree)
		self.pattern = pattern
		self.patternLength = len(self.pattern)
		self.charachterIndex = 0
		self.matches = []


	def traverseEdge(self, start, end):
		k = start
		while (k <= end and self.charachterIndex < self.patternLength):
			if(self.string[k] != self.pattern[self.charachterIndex]):
				return -1
			k += 1
			self.charachterIndex += 1
		if(k == self.patternLength):
			return 1
		return 0
	
	def doTraversalToCountLeaf(self, node):
		if node is None:
			return -1
		if(node.suffixIndex > -1):
			self.matches.append(node.suffixIndex)
			return
		
		for child in node.children.values():
			if(child is not node):
				self.doTraversalToCountLeaf(child)
		return
	
	def countLeaf(self, node):
		if node is None:
			return -1
		return self.doTraversalToCountLeaf(node)
	
	def doTraversal(self, node):
		
		if node is None:
			return -1
		
		res = -1
		if node.start != -1:
			res = self.traverseEdge(node.start, node.end)
			if res == -1:
				""" no match found """
				return -1
			if res == 1:
				""" match found let's find index of match(or matches) """
				if node.suffixIndex > -1:
					return [node.suffixIndex]
				else:
					self.countLeaf(node)
					return self.matches
		
		self.charachterIndex += node.edge_length()
		if(node.children[self.pattern[self.charachterIndex]]):
			return self.doTraversal(node.children[self.pattern[self.charachterIndex]])
		else:
			return -1

	def search(self):
		self.charachterIndex = 0
		return self.doTraversal(self.root)
