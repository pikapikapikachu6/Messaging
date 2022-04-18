from asyncio import tasks

from flask import Flask, request, abort, jsonify
import hashlib
import sql

app = Flask(__name__)


# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------

def init_database():
    global db
    db = sql.SQLDatabase()
    db.database_setup()


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/register', methods=['POST'])
def register():
    print(request.json)
    username = request.json['username']
    pwd = request.json['password']
    if db.check_username(username):
        db.add_user(username, pwd, 0)
        result = 'success'
    else:
        result = 'username has exists'
    return result


if __name__ == '__main__':
    init_database()
    app.run(host='127.0.0.1', port=80, debug=True)
