#!/usr/bin/env python3.8

from flask import Flask, jsonify

app = Flask(__name__)

USERS_ID = {}


@app.route("/vk_id/<username>", methods=["GET"])
def get_user_vk_id(username):
    if user_id := USERS_ID.get(username):
        return jsonify({"vk_id": str(user_id)}), 200
    else:
        return jsonify({}), 404


app.run(host='0.0.0.0', port=9000)
