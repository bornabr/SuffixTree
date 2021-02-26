# Suffix Tree

SuffixTree is a Python library for generating suffix trees and generalized suffix trees. also, there are helpers for pattern searching, finding the longest common substring, the longest repeated substring, and the longest palindromic substring.

## Installation

For using TestGUI you need to install docker and docker-compose first.
[Get Docker](https://docs.docker.com/get-docker/)

## Usage
For GUI testing
If you have installed docker and docker compose do the following:
```bash
./run start
```
or
```bash
docker-compose up
```
and if you do not have docker and docker compose
```bash
python -m pip install -r requirements.txt && python app.py
```
then you could open [http://localhost:5000](http://localhost:5000) in your browser and continue.
#
```python
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
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)