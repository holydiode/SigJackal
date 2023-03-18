from flask import Flask
from flask import request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return jsonify({'version': 1})


def main():
    app.run(host='45.9.41.222', port=80)

if __name__ == '__main__':
    main()
