# Suffix Tree

SuffixTree is a Python library for generating suffix trees and generalized suffix trees. also, there are helpers for pattern searching, finding the longest common substring, the longest repeated substring, and the longest palindromic substring.

## Installation

For using TestGUI you need to install docker and docker-compose first.
[Get Docker](https://docs.docker.com/get-docker/)

## Usage

```python
from suffixTree.suffixTree import SuffixTree
from suffixTree.helpers.searchPattern import SearchPattern
from suffixTree.helpers.lrs import LRS
from suffixTree.helpers.lcs import LCS

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
```
#
For using TestGUI
```bash
./run start
```
or
```bash
cd TestGUI
docker-compose up
```
then you could open [http://localhost:5000](http://localhost:5000) in your browser and continue.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)