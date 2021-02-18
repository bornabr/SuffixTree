from flask import Flask, render_template

PORT = 5000
HOST = '0.0.0.0'
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
