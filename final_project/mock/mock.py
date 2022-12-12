#!/usr/bin/env python3.8
import sqlalchemy
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/vk_id/<username>", methods=["GET"])
def get_user_vk_id(username):
    url = f'mysql+pymysql://test_qa:qa_test@mysql_host:3306/vkeducation'
    connection = sqlalchemy.create_engine(url).connect()
    result = connection.execute(f'SELECT id FROM test_users WHERE username="{username}"').fetchone()
    if result:
        return jsonify({"vk_id": str(result[0])}), 200
    else:
        return jsonify({}), 404


app.run(host='0.0.0.0', port=9000)
