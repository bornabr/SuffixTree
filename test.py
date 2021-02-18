from suffixTree.suffixTree import SuffixTree
from suffixTree.helpers.searchPattern import SearchPattern

tree = SuffixTree(["Geeksatb", "batl"], True)
# tree.print_dfs()

search = SearchPattern(tree, "at")
print(search.search())
