from suffixTree.suffixTree import SuffixTree
from suffixTree.helpers.searchPattern import SearchPattern
from suffixTree.helpers.lrs import LRS
from suffixTree.helpers.lcs import LCS
from suffixTree.helpers.lps import LPS

tree = SuffixTree(["Geeksatb", "batl"], True)

search = SearchPattern(tree, "at")
print(search.search())

""" Output
	{'1': [1], '0': [5]}
"""

tree = SuffixTree(["abcpqrabcpqpq"], True)

lrs = LRS(tree, 2)
print(lrs.find())

""" Output
	abcpq
"""

tree = SuffixTree(["xabxac", "abcabxabcd"], True)

lcs = LCS(tree, 2)
print(lcs.find())

""" Output
	abxa
"""

tree = SuffixTree(["xababayz"], True, True)

lps = LPS(tree)
print(lps.find())

""" Output
	ababa
"""
