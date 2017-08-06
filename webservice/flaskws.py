#!/usr/bin/env python
'''
ubuntu:
 sudo apt install python-pip
 dima@LAPTOP-MA6OEPO9:~/development/pxs_coding_challenge/webservice$ pip install flask
 dima@LAPTOP-MA6OEPO9:~/development/pxs_coding_challenge/webservice$ sudo pip install --upgrade pip
 dima@LAPTOP-MA6OEPO9:~/development/pxs_coding_challenge/webservice$ ./flaskws.py
 
 /home/dima/.cache
 
dima@LAPTOP-MA6OEPO9:~$ curl -X POST -H "Content-Type: application/json" -d '{"message":"foo"}' http://127.0.0.1:5000/messages/
{
  "digest": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"
}

curl -i http://127.0.0.1:5000/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae

'''

from flask import Flask, request, abort, make_response,jsonify
import flask
import hashlib

app = Flask(__name__)

messages = {}

@app.route('/', methods=["GET"])
def index():
    return "Hello, World!"

@app.route('/version/', methods=["GET"])
def get_version():
    return jsonify({"flask_version":flask.__version__})

@app.route('/messages/', methods=['GET'])
def get_messages():
    return jsonify({'messages': messages})

@app.route('/messages/<string:digest>', methods=['GET'])
def digest_to_message(digest):
    msg=messages.get(digest)
    if msg == None:
        return jsonify({"err_msg": "Message not found"}), 404
    else:
        return jsonify({"message":msg})

@app.route('/messages/', methods=['POST'])
def msg_to_digest():
    assert(request.method == 'POST')

    request_json=request.get_json()
    #msg=request_json.get('message','message not provided')
    msg = request_json.get('message')
    if msg == None:
        return jsonify({"err_msg": "message not passed.Usage:curl -X POST -H 'Content-Type: application/json' -d '{'message':'foo'}' "}), 404

    hash = hashlib.sha256(msg)
    digest = hash.hexdigest()
    messages[digest] = msg
    return jsonify({"digest":digest})

app.run(debug=True)
