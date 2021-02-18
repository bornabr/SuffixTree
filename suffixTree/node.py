#!/usr/bin/env python3

from operator import attrgetter

class Node:
	"""The Suffix-tree's node."""

	def __init__(self, tree, leaf):
		self.children = {}
		self.leaf = leaf
		self.suffixIndex = None
		self.start = None
		self.end = None 
		self.suffixLink = None
		self.tree = tree

	def edge_length(self):
		if(self == self.tree.root):
			return 0
		return self.end - self.start + 1

	def __eq__(self, node):
		atg = attrgetter('start', 'end', 'suffixIndex')
		return atg(self) == atg(node)

	def __ne__(self, node):
		atg = attrgetter('start', 'end', 'suffixIndex')
		return atg(self) != atg(node)

	def __getattribute__(self, name):
		if name == 'end':
			if self.leaf:
				return self.tree.leafEnd
		return super(Node, self).__getattribute__(name)
