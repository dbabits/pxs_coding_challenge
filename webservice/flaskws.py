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

'''
from flask import Flask
import hashlib
app = Flask(__name__)
 
@app.route('/', methods=["GET"])
def index():
    hash=hashlib.sha256(b'foo')
    hex=hash.hexdigest()
    return "Hello World. sha256(foo)="+hex
app.run(debug=True)
