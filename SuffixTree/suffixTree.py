#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from .node import Node


class SuffixTree:
	"""The Generilized Suffix Tree"""

	def __init__(self, strings: list, buildNow=False):
		self.terminalSymbolsGenerator = self._terminalSymbolsGenerator()
		
		self.strings = list()
		for string in strings:
			self.strings.append(string + self.terminalSymbolsGenerator.__next__())
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
		self.leafEnd += 1

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
				self.activePoint["node"].children[self.activePoint["edge"]] = splitNode
				splitNode.children[self.string[next_node.start]] = self.new_node(phase, leaf=True)
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
			

	def build(self):
		self.rootEnd = -1
		self.leafEnd = -1
		self.root = self.new_node(-1, self.rootEnd)
		self.activePoint["node"] = self.root
		for phase in range(self.size):
			self.extend(phase)
	
	def walk_dfs(self, current):
		start, end = current.start, current.end
		yield self.string[start: end + 1]

		for node in current.children.values():
			if node:
				yield from self.walk_dfs(node)
	
	def print_dfs(self):
		for sub in self.walk_dfs(self.root):
			print(sub)

if __name__ == '__main__':
	tree = SuffixTree(["abcabxabcd"], True)
	tree.print_dfs()
