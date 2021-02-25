from flask import Flask, render_template, jsonify, request

from suffixTree.suffixTree import SuffixTree
from suffixTree.helpers.searchPattern import SearchPattern
from suffixTree.helpers.lrs import LRS

from fastaParser import SimpleFastaParser

PORT = 5000
HOST = '0.0.0.0'
app = Flask(__name__)


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
    result = {'tree_simple_view': tree.simple_view(),
              'result': checker.search()}
    print(result)
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
    result = {'tree_simple_view': tree.simple_view(),
              'result': checker.find()}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
