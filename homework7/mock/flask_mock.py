#!/usr/bin/env python3
import json
import threading
from flask import Flask, jsonify, request

import settings

app = Flask(__name__)

app_data = {}
user_id_seq = 0


@app.route('/', methods=['GET'])
def get_users():
    return jsonify(app_data), 200


@app.route('/add_user', methods=['POST'])
def create_user():
    global user_id_seq
    user_name = json.loads(request.data)['name']
    if user_name not in app_data.values():
        user_id_seq += 1
        app_data[user_id_seq] = user_name
        return jsonify({'id': user_id_seq}), 201
    else:
        return jsonify(f'User_name {user_name} already exists: id:'), 400


@app.route('/get_user/<user_id>', methods=['GET'])
def get_user(user_id):
    user_id_int = int(user_id)
    if app_data.get(user_id_int):
        data = {'id': user_id_int,
                'name': app_data[user_id_int]}
        return jsonify(data), 200
    else:
        return jsonify(f'User with id {user_id} not found'), 404


@app.route('/edit_user/<user_id>', methods=['PUT'])
def edit_user(user_id):
    if app_data.get(user_id):
        app_data[user_id] = json.loads(request.data)['name']
        data = {'id': user_id,
                'name': app_data[user_id]}
        return jsonify(data), 200
    else:
        return jsonify(f'User with id {user_id} not found'), 404


@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if app_data.get(user_id):
        app_data.pop(user_id)
        return jsonify(user_id), 200
    else:
        return jsonify(f'User with id {user_id} not found'), 404


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()
    else:
        raise RuntimeError('Not running with the Werkzeug Server')


@app.route('/shutdown')
def shutdown():
    shutdown_stub()
    return jsonify(f'Ok, exiting'), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })

    server.start()
    return server


if __name__ == '__main__':
    run_mock()
