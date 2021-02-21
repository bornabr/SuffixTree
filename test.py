from suffixTree.suffixTree import SuffixTree
from suffixTree.helpers.searchPattern import SearchPattern
from suffixTree.helpers.lrs import LRS
from suffixTree.helpers.lcs import LCS

# tree = SuffixTree(["Geeksatb", "batl"], True)

# search = SearchPattern(tree, "at")
# print(search.search())

# tree = SuffixTree(["abcpqrabcpqpq"], True)

# lrs = LRS(tree, 2)
# print(lrs.find())

tree = SuffixTree(["xabxac", "abcabxabcd"], True)

lcs = LCS(tree, 2)
print(lcs.find())
