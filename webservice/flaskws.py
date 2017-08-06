#!/usr/bin/env python
'''
ubuntu:
 sudo apt install python-pip
 dima@LAPTOP-MA6OEPO9:~/development/pxs_coding_challenge/webservice$ pip install flask
 dima@LAPTOP-MA6OEPO9:~/development/pxs_coding_challenge/webservice$ sudo pip install --upgrade pip
 dima@LAPTOP-MA6OEPO9:~/development/pxs_coding_challenge/webservice$ ./flaskws.py
 
 /home/dima/.cache
 
 >>> import hashlib, binascii
>>> dk = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
>>> binascii.hexlify(dk)
b'0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5'

curl -X POST -H "Content-Type: application/json" -d '{"message":"foo"}' http://127.0.0.1:5000/messages/ 
curl http://127.0.0.1:5000/messages/

'''

from flask import Flask, request, abort, make_response
import hashlib

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return "Hello, World!"


@app.route('/messages/', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        #note = request.data.get('message', '')
		request_json=request.get_json()
		msg=request_json.get('message','message not provided')

        # idx = max(notes.keys()) + 1
        # notes[idx] = note
        # return note_repr(idx), status.HTTP_201_CREATED
		return msg

    hash = hashlib.sha256(b'foo')
    hex = hash.hexdigest()
    return hex


app.run(debug=True)
