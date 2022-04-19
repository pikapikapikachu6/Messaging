from asyncio import tasks
from random import getrandbits
import base64
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

from flask import Flask, request, abort, jsonify
import hashlib
import string
import random
import ssl
import socket

# -----------------
# Own python file
import sql

# -------------------
app = Flask(__name__)


@app.route('/api/register', methods=['POST'])
def register():
    username = request.json['username']
    pwd = request.json['password']
    print(username, pwd)
    if db.check_username(username):
        print("Success check username")
        db.add_user(username, pwd)
        result = 'success'
        print("success")
    else:
        result = 'username has exists'
    return result


@app.route('/api/login-first', methods=['POST'])
def login1():
    """
    Input: Username
    Output: result, username, random
    Flow:
    1.check Certification
    2.Record username
    3.Generate random
    4.return result
    """
    username = request.json['username']
    random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    if db.check_username(username):
        result = {
            'result': False,
            'username': None,
            'random': random_str
        }
        return result
    else:
        username_random[username] = random_str
        print(username, random_str, username_random)
        result = {
            'result': True,
            'username': username,
            'random': random_str
        }
        return result

    # if check_cert():
    #     print("Correct")
    #     username = request.json['username']
    #     random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    #     username_random[username] = random_str
    #     print(username, random_str, username_random)
    #     result = {
    #         'result': True,
    #         'username': username,
    #         'random': random_str
    #     }
    #     return result
    # else:
    #     result = {
    #         'result': False,
    #         'username': None,
    #         'random': None
    #     }
    #     return result


@app.route('/api/login-second', methods=['POST'])
def login2():
    """
    Input: user_pwd = hash(pwd, random), public key
    Output: Boolean
    flow:
    1.Record public key
    2.db_pwd = Hash(db.pwd, random)
    3.db_pwd ? user_pwd
    """
    # Input
    username = request.json['username']
    user_pwd = request.json['password']
    print("db username : ")
    print(username)
    print("db password : ")
    print(user_pwd)
    # public_key = request.json['public_key']

    # encry
    random_str = username_random[username]
    print("db random_str : ")
    print(random_str)
    db_pwd = db.get_pwd(username)[0]
    print("db password : ")
    print(db_pwd)
    db_pwd_salt = db_pwd + random_str
    print("db db_pwd_salt : ")
    print(db_pwd_salt)
    data_sha = base64.b64encode(hashlib.sha256(db_pwd_salt.encode('utf-8')).digest()).decode('ascii')
    print("db data_sha : ")
    print(data_sha)
    # RSA encryption
    # encrypt_data = encrypt_data(public_key, db_pwd_salt)
    if user_pwd == data_sha:
        return "true"
    else:
        return "false"


@app.route('/api/check-friend', methods=['POST'])
def check_friend():
    username = request.json['username']
    print(username)
    if db.check_username(username):
        result = "false"
    else:
        result = username
    return result


@app.route('/api/add-friend', methods=['POST'])
def add_friend_to_database():
    username = request.json['username']
    friend = request.json['friend']
    print(username)
    if db.check_username(username):
        return "false"
    else:
        if db.add_friend(username, friend):
            return "true"
    return "false"


def check_cert():
    # Host name should be ours
    hostname = "http://127.0.0.1"
    port = 80
    context = ssl.create_default_context()
    sockets = context.wrap_socket(socket.socket(), server_hostname=hostname)
    sockets.bind((hostname, port))
    try:
        cert = sockets.getpeercert()
    except ValueError:
        cert = None
    print(cert)
    # Wrong certication
    if cert is None:
        return False
    return True


# RSA encryption
def encrypt_data(public_key, msg):
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
    return encrypt_text.decode('utf-8')


if __name__ == '__main__':
    db = sql.SQLDatabase()
    db.database_setup()
    username_random = {}
    app.run(host='0.0.0.0', port=80, debug=True)
