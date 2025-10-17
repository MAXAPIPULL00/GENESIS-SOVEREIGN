# app.py: hello_world_rest_api/app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello_world():
    """Return a greeting message."""
    return jsonify({'message': 'Hello, World!'})

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    """Return a success response indicating the API's status."""
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    app.run(debug=True)