from suffixTree.suffixTree import SuffixTree
from suffixTree.helpers.searchPattern import SearchPattern

tree = SuffixTree(["GEEKSFORGEEKS"], True)
# tree.print_dfs()

search = SearchPattern(tree, "G")
print(search.search())
