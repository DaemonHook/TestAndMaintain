from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from DataLoader import *
from Algo import *

app = Flask(__name__)

CORS(app)


@app.route('/data')
def get_data():
    return origin_data


@app.route('/transfer', methods=['GET'])
def get_transfer():
    threshold = int(request.args.get('threshold'))
    if threshold <= 0:
        AutoSetShardThreshold()
    else:
        NODE_SHARD_THRESHOLD = threshold
    return GetTransferList(originState)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
