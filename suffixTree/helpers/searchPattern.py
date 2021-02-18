from .base import Base

class SearchPattern(Base):
	def __init__(self, tree, pattern):
		super(SearchPattern, self).__init__(tree)
		self.stringsRange = []
		index = 0
		for string in self.tree.strings:
			length = len(string)
			self.stringsRange.append((index, index + length - 2))
			index += length
		self.pattern = pattern
		self.patternLength = len(self.pattern)
		self.matches = []

	def traverseEdge(self, start, end, charachterIndex):
		k = start
		while (k <= end and charachterIndex < self.patternLength):
			# print('if', self.pattern[charachterIndex], self.string[k])
			if(self.string[k] != self.pattern[charachterIndex]):
				return -1
			k += 1
			charachterIndex += 1
		if(charachterIndex == self.patternLength):
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
	
	def doTraversal(self, node, charachterIndex):
		
		if node is None:
			return -1
		
		res = -1
		# print(node)
		if node.start != -1:
			res = self.traverseEdge(node.start, node.end, charachterIndex)
			# print('res', res)
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
		
		charachterIndex += node.edge_length()
		# print(charachterIndex)
		if(node.children.get(self.pattern[charachterIndex])):
			return self.doTraversal(node.children.get(self.pattern[charachterIndex]), charachterIndex)
		else:
			return -1

	def search(self):
		positions = self.doTraversal(self.root, 0)
		if(positions == -1):
			return -1
		result = dict()
		for position in positions:
			for index, (start, end) in enumerate(self.stringsRange):
				if start <= position <= end:
					if(result.get(str(index))):
						result.get(str(index)).append(position - start)
					else:
						result[str(index)] = []
						result.get(str(index)).append(position - start)
					break
		return result
