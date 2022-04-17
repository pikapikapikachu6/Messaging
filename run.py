from asyncio import tasks

from flask import Flask, request, abort, jsonify
import hashlib

app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/register', methods=['POST'])
def register():
    print(request.headers)
    print(request.values)
    # print request.form.get('name')
    # print request.form.getlist('name')
    # print request.form.get('nickname', default='little apple')
    return request.json['firstname']


@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)
