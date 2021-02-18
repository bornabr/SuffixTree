from flask import Flask, render_template, jsonify, request
from suffixTree.suffixTree import SuffixTree
from suffixTree.helpers.searchPattern import SearchPattern

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
	strings = strings.split('>\n')
	tree = SuffixTree(strings, True)
	pattern = request.form.get('pattern')
	if(pattern is None or pattern == ''):
		pattern = ''
	checker = SearchPattern(tree, pattern)
	result = {'tree': tree.__dict__(),
			  'result': checker.search()}
	print(result)
	return jsonify(result)


if __name__ == '__main__':
	app.run(host=HOST, port=PORT)
