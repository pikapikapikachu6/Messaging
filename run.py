# -*- coding: UTF-8 -*-
import base64
import hashlib
import os
import random
import re
import socket
import ssl
import string
from turtle import pos
from xml.etree.ElementTree import Comment

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from flask import Flask, request, jsonify

# -----------------
# Own python file
import sql

# -------------------
app = Flask(__name__)


@app.route('/api/register', methods=['POST'])
def register():
    # print("In register:")
    username = request.json['username']
    pwd = request.json['password']
    # print('username: ' + username)
    # print('pwd: ' + pwd)
    if db.check_username(username):
        pk = load_key("pk")
        # print("Check username is unique successfully!")
        db.add_user(username, pwd)
        result = {
            'result': 'success',
            'public_key': pk
        }
    else:
        result = {
            'result': 'username has exists',
            'public_key': 'None'
        }
    # print("Result:", result['result'], result['public_key'])
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
    # Check CA
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
        if (len(result) == 0):
            result = ""
        else:
            for node in result:
                print(node)
                if (len(res) == 0):
                    res += str(node[0])
                else:
                    res = res + ' ' + str(node[0])
        print("res:" + res)
    return res


# # Generate a certification
# # Store the key in the files
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


# return the public key
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
user_msg = {}  # {(sender, receiver): [messages]}

# 已下线用户
out_msg = {}  # {(sender, receiver): [messages]} (sender, receiver) share (receiver, sender)


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
    # time = request.json.get("time")

    user_tut = check_name(sender_username, receiver_username)
    if user_tut in user_msg:
        user_msg[user_tut].append(message)
        histroy[user_tut].append(message)
    else:
        user_msg[user_tut] = message
        histroy[user_tut] = message

    # Reduce the message
    if len(user_msg[user_tut]) > 100:
        half = int(len(user_msg[user_tut]) / 2)
        user_msg[user_tut] = user_msg[user_tut][half:]
        histroy[user_tut] = histroy[user_tut][half:]

    return jsonify({
        "status": 1,
        "error": "",
        "message": "",
    })

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


@app.route('/api/getPK', methods=['POST'])
def get_friendPK():
    print(username_public)
    username = request.json['username']
    print("username:" + username)
    if db.check_username(username):
        return "false"
    else:
        result = username_public[username]
        print("friend pk: " + result)
    return result


# {(sender, receiver): [messages]}
@app.route('/api/post_mess_DB', methods=['POST'])
def get_post_mess_db():
    sender = request.json['sender']
    receiver = request.json['receiver']
    message = request.json['message']
    sen_rec = (sender, receiver)
    print("username:" + sender)
    print("receiver:" + receiver)
    print("message:" + message)
    print("sen_rec:")
    print(sen_rec)
    if sen_rec in user_msg:
        user_msg[sen_rec].append(message)
    else:
        mes = [message]
        user_msg[sen_rec] = mes
    print("user_msg:  ")
    print(user_msg)
    return "true"


@app.route('/api/get_all_message', methods=["POST"])
def get_receive_message():
    """
    message
    """
    sender = request.json['sender']
    receiver = request.json['receiver']
    sen_rec = (sender, receiver)
    message_list = []
    if sen_rec in user_msg:
        if len(user_msg[sen_rec]) == 100:
            message_list = user_msg[sen_rec][90:]
        else:
            message_list = user_msg[sen_rec]
    return jsonify(message_list)

@app.route('/api/create-post', methods=["POST"])
def create_post():
    title = request.json['title']
    content = request.json['content']
    creator = request.json['creator']
    post_content = (title, content, creator)
    id = len(post)
    post[id] = post_content
    print(title)
    print(content)
    print(creator)
    print(post)

    return "true"

@app.route('/api/get-post', methods=["GET"])
def get_post():
    return post

@app.route('/api/delete-post', methods=["POST"])
def delete_post():
    #find id, delete id, re-arrange
    title = request.json['title']
    content = request.json['content']
    creator = request.json['creator']
    post_content = (title, content, creator)
    post_id = -1
    #find id
    for key, value in post.items():
        print(key)
        if value == post_content:
            post_id = key
            break
    #delete id.
    if post_id != -1:
        post.pop(post_id)
        #re-arrange
        new_post = {}
        for id, content in post.items():
            new_id = len(new_post)
            new_post[new_id] = content
        post = new_post
    return "true"


@app.route('/api/add-comment', methods=["POST"])
def add_comment():
    title = request.json['title']
    if request.json['content'] == None:
        content = None
    else:
        content = request.json['content'] #the post information
    creator = request.json['creator'] #The post author
    comment = request.json['comment'] #The comment content
    name = request.json['name'] #The commenter name
    post_content = (title, content, creator)
    post_id = -1
    #find id
    for key, value in post.items():
        print(key)
        if value == post_content:
            post_id = key
            break
    #add information into the comment
    new_comment = (name, comment)
    if post_id in post_comment:
        post_comment[post_id].append(new_comment)
    else:
        print("?")
        post_comment[post_id] = [new_comment]
    print(post_comment)
    print(post_comment[post_id])
    #return the comment
    id_str = str(post_id)
    return id_str
    
@app.route('/api/get-comment', methods=["POST"])
def get_comment():
    id = request.json['id']
    if id == -1:
        return post_comment
    id = int(id)
    return {id:post_comment[id]}


if __name__ == '__main__':
    db = sql.SQLDatabase()
    db.database_setup()
    username_random = {}  # The username with corresponding random string
    username_public = {}  # The useranme with corresponding public key
    post = {}
    post_comment = {} # post_id : [(author, comment information)] eg. 1: [(Tom, "Hello"), (Tom, "World")] 
    generate_cert()
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
