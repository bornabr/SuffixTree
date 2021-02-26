from flask import Flask, render_template, jsonify, request

from suffixTree.suffixTree import SuffixTree
from suffixTree.helpers.searchPattern import SearchPattern
from suffixTree.helpers.lrs import LRS
from suffixTree.helpers.lcs import LCS
from suffixTree.helpers.lps import LPS

from fastaParser import SimpleFastaParser

from io import StringIO

from pptree import print_tree

import sys

PORT = 5000
HOST = '0.0.0.0'
app = Flask(__name__)


def simple_view(tree):
	old_stdout = sys.stdout
	new_stdout = StringIO()
	sys.stdout = new_stdout

	print_tree(tree.root, 'childrenArray')

	output = new_stdout.getvalue()

	sys.stdout = old_stdout

	return output

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/api/search-pattern', methods=['POST'])
def search_pattern():
    strings = request.form.get('strings')
    if(strings is None or strings == ''):
        strings = ''
    strings = strings.splitlines()
    strings = [(title, sequence)
               for title, sequence in SimpleFastaParser(strings)]
    tree = SuffixTree(strings, True)
    pattern = request.form.get('pattern')
    if(pattern is None or pattern == ''):
        pattern = ''
    checker = SearchPattern(tree, pattern)
    result = {'tree_simple_view': simple_view(tree),
              'result': checker.search()}
    return jsonify(result)


@app.route('/api/lrs', methods=['POST'])
def lrs():
    strings = request.form.get('strings')
    if(strings is None or strings == ''):
        strings = ''
    strings = strings.splitlines()
    strings = [(title, sequence)
               for title, sequence in SimpleFastaParser(strings)]
    tree = SuffixTree(strings, True)
    k = request.form.get('k')
    if(k is None or k == ''):
        k = 0
    k = int(k)
    checker = LRS(tree, k)
    result = {'tree_simple_view': simple_view(tree),
              'result': checker.find()}
    return jsonify(result)


@app.route('/api/lcs', methods=['POST'])
def lcs():
    strings = request.form.get('strings')
    if(strings is None or strings == ''):
        strings = ''
    strings = strings.splitlines()
    strings = [(title, sequence)
               for title, sequence in SimpleFastaParser(strings)]
    tree = SuffixTree(strings, True)
    k = request.form.get('k')
    if(k is None or k == ''):
        k = 0
    k = int(k)
    checker = LCS(tree, k)
    result = {'tree_simple_view': simple_view(tree),
              'result': checker.find()}
    return jsonify(result)

@app.route('/api/lps', methods=['POST'])
def lps():
    strings = request.form.get('strings')
    if(strings is None or strings == ''):
        strings = ''
    strings = strings.splitlines()
    strings = [(title, sequence)
               for title, sequence in SimpleFastaParser(strings)]
    tree = SuffixTree(strings, True, True)
    checker = LPS(tree)
    result = {'tree_simple_view': simple_view(tree),
              'result': checker.find()}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
