import flask
from flask import request, jsonify, make_response
import numpy as np
import json
from functools import wraps
from werkzeug.exceptions import BadRequest
from flask_expects_json import expects_json

app = flask.Flask(__name__)
app.config["DEBUG"] = False
pools = {}

schema_append = {
    'type': 'object',
    'properties': {
        'poolId': {'type': 'integer', "pattern": "^[0-9]+$"},
        'poolValues': {'type': 'array',
                       "items": {"type": "integer"}
                       }
    },
    'required': ['poolId', 'poolValues']
}

# poolId only type int
# percentile only type number
schema_get = {
    'type': 'object',
    'properties': {
        'poolId': {'type': 'integer', "pattern": "^[0-9]+$"},
        'percentile': {'type': 'number', "minimum": 0, "maximum": 100}
    },
    'required': ['poolId', 'percentile']
}


# If the data isn't JSON, return an error code 400, which is the code for the bad request.
def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except BadRequest:
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        return f(*args, **kw)

    return wrapper


def quantile(x, p):
    # quantile is lower value between two data points i < j(which is same as np.quantile as param interpolation='lower')
    # minimum of index is 0
    p_index = max(int(np.floor(p * len(x))) - 1, 0)
    return x[p_index]


def append_values(exits_pool_values, new_values):
    # check for the smaller of two element on the current index and increment the index of the list whose no. is encountered.
    # When either of the list gets exhausted, the other list is appended to the end of merged list.
    size_exits_pool = len(exits_pool_values)
    size_new_values = len(new_values)
    res = []
    i, j = 0, 0

    while i < size_exits_pool and j < size_new_values:
        if exits_pool_values[i] < new_values[j]:
            res.append(exits_pool_values[i])
            i += 1

        else:
            res.append(new_values[j])
            j += 1

    res = res + exits_pool_values[i:] + new_values[j:]
    return res


def response(json_resp, status_code):
    resp = make_response(json.dumps(json_resp), status_code)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/get_quantile', methods=['POST'])
@validate_json
@expects_json(schema_get)
def get_quantile():
    # If the data isn't JSON, return an error code 400, which is the code for the bad request.
    pool_request = request.get_json()
    pool_id = str(int(pool_request["poolId"]))
    percentile = pool_request["percentile"] / 100
    pool_values = pools[pool_id]
    res = {"total_number_elements": len(pool_values), "quantile": quantile(pool_values, percentile),
           "values": pool_values}
    return response(res, 200)


@app.route('/pools', methods=['POST'])
@validate_json
@expects_json(schema_append)
def add_pool():
    resp = {}
    # request
    data = request.get_json()
    pool_id = str(int(data["poolId"]))
    new_values = sorted(data["poolValues"])

    if pool_id in pools:
        pools[pool_id] = append_values(pools[pool_id], new_values)
        resp["status"] = "appended"
    else:
        pools[pool_id] = new_values
        resp["status"] = "inserted"
    return response(resp, 200)


if __name__ == '__main__':
    app.run()
