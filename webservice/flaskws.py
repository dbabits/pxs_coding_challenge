#!/usr/bin/env python

from flask import Flask, request, abort, make_response,jsonify
import hashlib

app = Flask(__name__)

messages = {}

@app.route('/', methods=["GET"])
def index():
    return '''
    <pre>
    Installation on Ubuntu:
         sudo apt install python-pip
         dima@LAPTOP-MA6OEPO9:~/development/pxs_coding_challenge/webservice$ pip install flask
         dima@LAPTOP-MA6OEPO9:~/development/pxs_coding_challenge/webservice$ sudo pip install --upgrade pip
         dima@LAPTOP-MA6OEPO9:~/development/pxs_coding_challenge/webservice$ ./flaskws.py

    Usage:     
        show this message:   
            curl -Li {url_root}
        show endpoints:   
            curl -Li {url_root}show_endpoints/
        set the message and get its digest: 
            curl -Li -X POST -H "Content-Type: application/json" -d '{{"message":"foo"}}' {url_root}messages/
        return the original message from digest(should return foo)"
            curl -Li {url_root}messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae
        list all messages saved:
            curl -Li {url_root}messages/
        
        host={host}
        url_root={url_root}
        
    '''.format(host=request.host,url_root=request.url_root)

@app.route('/show_endpoints/', methods=["GET"])
def show_endpoints():
    return "Implemented endpoints:\n" + str(app.url_map)+"\n\n"

@app.route('/version/', methods=["GET"])
def get_version():
    return jsonify({"flask_version":flask.__version__})

@app.route('/messages/', methods=['GET'])
def get_messages():
    return jsonify({'messages': messages})

@app.route('/messages/<string:digest>', methods=['GET'])
def digest_to_msg(digest):
    msg=messages.get(digest)
    if msg == None:
        return jsonify({"err_msg": "Message not found"}), 404
    else:
        return jsonify({"message":msg})

@app.route('/messages/', methods=['POST'])
def msg_to_digest():
    assert(request.method == 'POST')

    request_json=request.get_json()

    msg = request_json.get('message')
    if msg == None:
        return jsonify({"err_msg": "message not passed.Usage:curl -X POST -H 'Content-Type: application/json' -d '{'message':'foo'}' "}), 404

    hash = hashlib.sha256(msg)
    digest = hash.hexdigest()

    info=None
    if len(messages)>10000:
            messages.clear()
            info="All messages cleared because I can't afford more than 10000- this is not how I'd do it in real program. Sorry!  Scalability coming up.."

    messages[digest] = msg
    return jsonify({"digest":digest,"count(messages)":len(messages),"info":info})


app.run(debug=True)