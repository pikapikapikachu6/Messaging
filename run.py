from asyncio import tasks
from crypt import methods
import queue
from random import getrandbits
import base64
import uuid
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.Hash import SHA


from flask import Flask, request, abort, jsonify
import hashlib
import string
import random
import ssl
import socket
import os

# -----------------
# Own python file
import sql

# -------------------
app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
    print("In register")
    username = request.json['username']
    pwd = request.json['password']
    print(username, pwd)
    if db.check_username(username):
        pk = load_key("pk")
        print(pk)
        print("Success check username")
        db.add_user(username, pwd)
        result = {
            'result': 'success',
            'public_key': pk
        }
        print("success")
    else:
        result = {
            'result': 'username has exists',
            'public_key': 'None'
        }
    print("Result:", result['result'], result['public_key'])
    return result

@app.route('/api/login-first', methods=['POST'])
def login1():
    """
    Input: Username
    Output: result, username, random, server_ca
    Flow:
    1.check Certification
    2.Record username
    3.Generate random
    4.return result
    """
    #Check CA
    cipher = request.json['cipher']
    sk = load_key("sk")
    print(cipher)
    message = decrypt_data(sk, cipher)
    if message == "I am client":
        print("Success")
    else:
        result = {
            'result': "Is not a Certificate Authority",
            'username': None,
            'random': None
        }
        return result
    print(message)
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
    public_key = request.json['public_key']
    username_public[username] = public_key
    print("db public key array list: ")
    print(username_public)

    # encry
    random_str = username_random[username]
    print("db random_str : ")
    print(random_str)
    db_pwd = db.get_pwd(username)[0][0]
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
    print("add friend API starts:")
    username = request.json['username']
    friend = request.json['friend']
    print(username)
    print(friend)
    if db.add_friend(username, friend):
        print("add friend finished")
        print(db.get_friend(username))
        return "true"
    return "false"


@app.route('/api/get-friend-list', methods=['POST'])
def get_friend_list():
    username = request.json['username']
    print(username)
    if db.check_username(username):
        return "false"
    else:
        res = ''
        result = db.get_friend(username)
        if (len(result) == 0): result = ""
        else:
            for node in result:
                print(node)
                if (len(res) == 0):
                    res += str(node[0])
                else:
                    res = res + ' ' + str(node[0])
        print("res:" + res)
    return res

#Generate a certification
#Store the key in the files
def generate_cert():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    directory = "cert"
    if not os.path.isdir(directory):
        os.makedirs(directory)
    with open("cert/private.pem", "wb") as private_file:
        private_file.write(private_key)
    with open("cert/public.pem", "wb") as public_file:
        public_file.write(public_key)

#return the public key
def load_key(key):
    if key == "pk":
        pk = ""
        with open("cert/public.pem") as public_file:
            for line in public_file:
                pk += line
        return pk
    else:
        sk = ""
        with open("cert/private.pem") as private_file:
            for line in private_file:
                sk += line
        return sk

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

# RSA decryption
def decrypt_data(private_key, msg):
    decodeStr = base64.b64decode(msg)
    rsakey = RSA.importKey(private_key)
    prikey = Cipher_pksc1_v1_5.new(rsakey)
    encry_text = prikey.decrypt(decodeStr, b'rsa')
    return encry_text.decode('utf8')

histroy = {}  # 存储聊天记录，100条 #{(sender, receiver): [messages]}

# sender, receiver and their messages
user_msg = {} #{(sender, receiver): [messages]}

# 已下线用户
out_msg = {} #{(sender, receiver): [messages]} (sender, receiver) share (receiver, sender)


@app.after_request  # 解决CORS跨域请求
def cors(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    if request.method == "OPTIONS":
        response.headers["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token,authorization"
    return response

@app.route('/api/send_message', methods=["POST"])
def send_message():
    """
    input: sender_username, receiver_username. msg
    output: status
    """
    sender_username = request.json['sender_username']
    receiver_username = request.json['receiver_username']
    message = request.json['message']
    #time = request.json.get("time")

    user_tut = check_name(sender_username, receiver_username)
    if user_tut in user_msg:
        user_msg[user_tut].append(message)
        histroy[user_tut].append(message)
    else:
        user_msg[user_tut] = message
        histroy[user_tut] = message

    #Reduce the message
    if len(user_msg[user_tut]) > 100:
        half = int(len(user_msg[user_tut])/2)
        user_msg[user_tut] = user_msg[user_tut][half:]
        histroy[user_tut] = histroy[user_tut][half:]

    return jsonify({
        "status": 1,
        "error": "",
        "message": "",
    })

@app.route('/api/get_all_message', methods=["POST"])
def get_all_message():
    """
    message
    """
    global histroy
    if len(histroy) == 100:
        histroy = histroy[90:101]
    return jsonify(histroy)


"""
暂时无视这个，之后有时间再来完善这个方法
@app.route('/get_new_message', methods=["POST"])
def get_new_message():
    sender_username = request.json['sender_username']
    receiver_username = request.json['receiver_username']
    q = user_queue[username]
    try:
        # 获取不到就阻塞,不立即返回
        new_message_dic = q.get(timeout=30)
    except queue.Empty:
        return jsonify({
            "status": 0,
            "error": "没有新消息",
            "message": "",
        })
    return jsonify({
        "status": 1,
        "error": "",
        "message": new_message_dic
    })
"""
def check_name(sender, receiver):
    sender_tut = (sender, receiver)
    receiver_tut = (sender, receiver)

    if receiver_tut in user_msg:
        return receiver_tut
    return sender_tut

if __name__ == '__main__':
    db = sql.SQLDatabase()
    db.database_setup()
    username_random = {} #The username with corresponding random string 
    username_public = {} #The useranme with corresponding public key
    generate_cert()
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
