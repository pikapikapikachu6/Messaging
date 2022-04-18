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

#-----------------
#Own python file
import sql
#-------------------
app = Flask(__name__)


# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------

@app.route('/register', methods=['POST'])
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


@app.route('/login-first', methods=['POST'])
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
    if check_cert():
        print("Correct")
        username = request.json['username']
        random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        username_random[username] = random_str
        print(username, random_str, username_random)
        result = {
            'result': True,
            'username': username,
            'random': random_str
        }
        return result
    else:
        result = {
            'result': False,
            'username': None,
            'random': None
        }
        return result


@app.route('/login-second', methods=['POST'])
def login2():
    """
    Input: user_pwd = hash(pwd, random), public key
    Output: Boolean
    flow:
    1.Record public key
    2.db_pwd = Hash(db.pwd, random)
    3.db_pwd ? user_pwd
    """
    #Input
    username = request.json['username']
    user_pwd = request.json['password']
    public_key = request.json['public_key']

    #encry
    random_str = username_random[username]
    db_pwd = db.get_pwd(username)
    db_pwd_salt = db_pwd + random_str
    #RSA encryption
    encrypt_data = encrypt_data(public_key, db_pwd_salt)
    if user_pwd == encrypt_data:
        return True
    return False

def check_cert():
    #Host name should be ours
    hostname = "http://127.0.0.1"
    port = 3000
    context = ssl.create_default_context()
    sockets = context.wrap_socket(socket.socket(), server_hostname=hostname)
    sockets.connect((hostname, port))
    try:
        cert = sockets.getpeercert()
    except ValueError:
        cert = None
    print(cert)
    #Wrong certication
    if cert is None:
        return False
    return True

#RSA encryption
def encrypt_data(public_key, msg):
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
    return encrypt_text.decode('utf-8')

if __name__ == '__main__':
    db = sql.SQLDatabase()
    db.database_setup()
    username_random = {}
    app.run(host='127.0.0.1', port=80, debug=True)
