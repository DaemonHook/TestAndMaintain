from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from DataLoader import *
from Algo import *
from Schedule import SA_routine

app = Flask(__name__)


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
    return jsonify(GetTransferList(originState))


best_schedule = []


def set_best_schedule():
    global best_schedule
    print("Settting best schedule")
    best_schedule = SA_routine()
    print("Setting done!")


@app.route('/schedule', methods=['GET'])
def get_best_schedule():
    return jsonify(best_schedule)


@app.route('/reschedule', methods=['GET', 'POST'])
def reschedule():
    set_best_schedule()
    return None


set_best_schedule()

CORS(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
