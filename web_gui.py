from flask import Flask
from flask import request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return jsonify({'version': -2})


def main():
    app.run(debug=True, port=8080, host='0.0.0.0')

if __name__ == '__main__':
    main()
