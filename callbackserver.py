"""
simple server

Acts a enging for the remote system

A html5 page can be fetched at port 5000. Using chrome version 25 or above enables user to send
voice commands back to the server.

The server uses a websocket for communication with the webpage

A object called TheBrain hendles the logic. I gets all the voice commands from the user and responds.
"""
from flask import Flask
from flask_sockets import Sockets

# this is for launching the server handling the websocket
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
sockets = Sockets(app)

writePermission = ["write permission","add device","11730"]
ownerName=["robert", "1302"]
password=["1023"]

from flask import render_template

# running for web page
@app.route('/')
def hello(name=None):

    # get the current ip to be used for socket connection
    import socket
    ip = socket.gethostbyname(socket.gethostname())

    return render_template('voice5.html', ip="94.255.149.252")

@sockets.route('/echo') #web socket will call ECHO
def echo_socket(ws):

    global brain

    while True:
        message = ws.receive().strip()

        ws.send("from server" + message)

if __name__ == '__main__':
    http_server = WSGIServer(('',80), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
