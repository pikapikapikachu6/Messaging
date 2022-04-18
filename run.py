from asyncio import tasks
from random import getrandbits

from flask import Flask, request, abort, jsonify
import hashlib
import sql
import string
import random

app = Flask(__name__)


# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------

def init_database():
    global db
    db = sql.SQLDatabase()
    db.database_setup()


@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    pwd = request.json['password']
    if db.check_username(username):
        db.add_user(username, pwd, 0)
        result = 'success'
    else:
        result = 'username has exists'
    return result


@app.route('/login-first', methods=['POST'])
def login1():
    username = request.json['username']
    random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    result = {
        'result': True,
        'username': username,
        'random': random_str
    }
    return result


if __name__ == '__main__':
    init_database()
    app.run(host='127.0.0.1', port=80, debug=True)
