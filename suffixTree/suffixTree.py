#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from .node import Node

from io import StringIO
from pptree import print_tree

class SuffixTree(object):
	"""The Generilized Suffix Tree"""

	def __init__(self, strings: list, buildNow=False, checkForPalindrom=False):
		self.terminalSymbolsGenerator = self._terminalSymbolsGenerator()
		self.checkForPalindrom = checkForPalindrom
		self.strings = list()
		self.titles = list()
		if self.checkForPalindrom:
			if isinstance(strings[0], tuple):
				self.strings.append(strings[0][1] + '#')
				self.strings.append(strings[0][1][::-1] + '$')
				self.titles.append(strings[0][0])
			else:
				self.strings.append(strings[0] + '#')
				self.strings.append(strings[0][::-1] + '$')
				self.titles.append('0')
		else:
			for index, string in enumerate(strings):
				if isinstance(string, tuple):
					self.strings.append(string[1] + self.terminalSymbolsGenerator.__next__())
					self.titles.append(string[0])
				else:
					self.strings.append(string + self.terminalSymbolsGenerator.__next__())
					self.titles.append(str(index))
		self.string = "".join(self.strings)
		self.lastNewNode = None

		""" active point is stored a dict {node, edge, length},
			also activeEdge is presented by input string index """
		self.activePoint = {
			"node": None,
			"edge": -1,
			"length": 0
		}

		""" remainingSuffixCount, to track how many extensions are yet to be performed explicitly in any phase """
		self.remainingSuffixCount = 0

		self.rootEnd = None
		self.size = len(self.string)  # Length of input string
		self.root = None
		if buildNow:
			self.build()

	def _terminalSymbolsGenerator(self):
		""" Generator of unique terminal symbols used for building the Generalized Suffix Tree.
		Unicode Private Use Area U+E000..U+F8FF is used to ensure that terminal symbols
		are not part of the input string. """
		py2 = sys.version[0] < '3'
		UPPAs = list(list(range(0xE000,0xF8FF+1)) + list(range(0xF0000,0xFFFFD+1)) + list(range(0x100000, 0x10FFFD+1)))
		# UPPAs = map(lambda x: ord(x), ["$", "#", "%"])
		for i in UPPAs:
			if py2:
				yield(unichr(i))
			else:
				yield(chr(i))
		raise ValueError("To many input strings.")

	def new_node(self, start, end=None, leaf=False):
		""" For root node, suffixLink will be set to NULL
		For internal nodes, suffixLink will be set to root
		by default in  current extension and may change in
		next extension """
		node = Node(self, leaf)
		node.suffixLink = self.root
		node.start = start
		node.end = end
		""" suffixIndex will be set to -1 by default and
		   actual suffix index will be set later for leaves
		   at the end of all phases """
		node.suffixIndex = -1
		return node

	def walk_down(self, current_node):
		""" Walk down from current node.
		activePoint change for walk down (APCFWD) using
		Skip/Count Trick  (Trick 1). If activeLength is greater
		than current edge length, set next  internal node as
		activeNode and adjust activeEdge and activeLength
		accordingly to represent same activePoint. """
		length = current_node.edge_length()
		if (self.activePoint["length"] >= length):
			self.activePoint["edge"] += length
			self.activePoint["length"] -= length
			self.activePoint["node"] = current_node
			return True
		return False
	
	def extend(self, phase):
		""" Extension Rule 1, this takes care of extending all
		leaves created so far in tree (trick 3 - Once a leaf, always a leaf) """
		self.leafEnd = phase

		self.remainingSuffixCount += 1

		""" Set lastNewNode to None while starting a new phase,
		indicating there is no internal node waiting for
		it's suffix link reset in current phase """
		self.lastNewNode = None

		""" Run a loop for the remaining extensions """
		while(self.remainingSuffixCount > 0):

			if (self.activePoint["length"] == 0):
				""" activePoint change for Active Length ZERO (APCFALZ) """
				self.activePoint["edge"] = phase

			if (self.activePoint["node"].children.get(self.string[self.activePoint["edge"]]) is None):
				""" There is no outgoing edge
				starting with activeEdge from activeNode """

				""" Extension Rule 2 (A new leaf edge gets created) """
				self.activePoint["node"].children[self.string[self.activePoint["edge"]]] = self.new_node(
					phase, leaf=True)

				if (self.lastNewNode is not None):
					""" If there is an internal node waiting for it's suffix link
					point the suffix link from that internal node to current active node """
					self.lastNewNode.suffixLink = self.activePoint["node"]
					self.lastNewNode = None
			else:
				""" There is an outgoing edge starting with activeEdge from activeNode """
				next_node = self.activePoint["node"].children.get(
					self.string[self.activePoint["edge"]])

				if(self.walk_down(next_node)):
					""" Start from the next_node """
					continue

				""" Extension Rule 3 (current character being processed
					is already on the edge) """

				if (self.string[next_node.start + self.activePoint["length"]] == self.string[phase]):

					if((self.lastNewNode is not None) and (self.activePoint['node'] != self.root)):
						""" If there is an internal node waiting for it's suffix link
							point the suffix link from that internal node to current active node """
						self.lastNewNode.suffixLink = self.activePoint["node"]
						self.lastNewNode = None

					""" Now it's time to go to next phase,
						we increament active length by one before that (APCFER3) """
					self.activePoint["length"] += 1
					break

				""" We will be here when activePoint is in middle of
					the edge being traversed and current character
					being processed is not on the edge (we fall off
					the tree). In this case, this is Extension Rule 2 """
				splitEnd = next_node.start + self.activePoint['length'] - 1
				splitNode = self.new_node(next_node.start, splitEnd)
				self.activePoint["node"].children[self.string[self.activePoint["edge"]]] = splitNode
				splitNode.children[self.string[phase]] = self.new_node(phase, leaf=True)
				next_node.start += self.activePoint['length']
				splitNode.children[self.string[next_node.start]] = next_node
				
				if (self.lastNewNode is not None):
					""" If there is an internal node waiting for it's suffix link
						point the suffix link from that internal node to new splitNode """
					self.lastNewNode.suffixLink = splitNode
				
				""" Now we set splitNode as the lastNewNode
					so that it's suffix like be set in the future """
				self.lastNewNode = splitNode
			
			""" One suffix got added in tree, decrement the count of
			   suffixes yet to be added. Note that this below code won't be run for APCFER3"""
			self.remainingSuffixCount -= 1
			
			if ((self.activePoint["node"] == self.root) and (self.activePoint['length'] > 0)):
				""" APCFER2C1 """
				self.activePoint['length'] -= 1
				self.activePoint["edge"] = phase - self.remainingSuffixCount + 1
			elif (self.activePoint["node"] != self.root):
				""" APCFER2C2 """
				self.activePoint["node"] = self.activePoint["node"].suffixLink
	
	
	def setSuffixIndexByDFS(self, node, labelHeight):
		if(node is Node):
			return
		
		isLeaf = True
		for child in node.children.values():
			isLeaf = False
			self.setSuffixIndexByDFS(child, labelHeight + child.edge_length())
			if node != self.root:
				node.forwardIndices = node.forwardIndices.union(child.forwardIndices)
				node.reverseIndices = node.reverseIndices.union(child.reverseIndices)
		if(isLeaf):
			for i in range(node.start, node.end + 1):
				if(self.string[i] == '#'):
					node.end = i
			node.suffixIndex = self.size - labelHeight
			
			if (node.suffixIndex < len(self.strings[0])):
				node.forwardIndices.add(node.suffixIndex)
			else:
				node.reverseIndices.add(node.suffixIndex - len(self.strings[0]))


	def build(self):
		self.rootEnd = -1
		self.leafEnd = -1
		self.root = self.new_node(-1, self.rootEnd)
		self.activePoint["node"] = self.root
		for phase in range(self.size):
			self.extend(phase)
		self.setSuffixIndexByDFS(self.root, 0)
	
	def walk_dfs(self, current, parent=None):
		start, end = current.start, current.end
		index = self.index
		self.nodes.append({ 'id': index, 'label': str(index) })
		if(parent is not None):
			self.edges.append({
				'from': parent,
				'to': index,
				'label': str(start) + ':' + str(end)
			})

		for node in current.children.values():
			self.index += 1
			self.walk_dfs(node, index)
	
	def __dict__(self):
		self.nodes = []
		self.edges = []
		self.index = 1
		self.walk_dfs(self.root)
		return {
			'nodes': self.nodes,
			'edges': self.edges
		}
	
	def __str__(self):
		return str(self.__dict__())

	def simple_view(self):
		old_stdout = sys.stdout
		new_stdout = StringIO()
		sys.stdout = new_stdout
		
		print_tree(self.root, 'childrenArray')
		
		output = new_stdout.getvalue()
		
		sys.stdout = old_stdout
		
		return output

if __name__ == '__main__':
	tree = SuffixTree(["abcabxabcd"], True)
	print(tree)
