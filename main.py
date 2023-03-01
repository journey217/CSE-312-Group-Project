from flask import Flask
import flask
import socketserver
from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client["CSE312-Group-Project-Test"]
master = db["Testing"]


app = Flask(__name__)


@app.route('/')
def return_html():  # Naming convention can be changed
    return flask.render_template('index.html')  # It renders the html, pycharm says there is an error


# @app.route('/style.css')
# def return_css():
#     return flask.render_template('style.css')

# class MyTCPHandler(socketserver.BaseRequestHandler):
#     socketserver.TCPServer.allow_reuse_address = True
#
#     def handle(self):
#         received_data = self.request.recv(2048)
#         dataInsert = {"Name": "Journey"}
#         master.insert_one(dataInsert)
#         self.request.sendall(
#             f'HTTP/1.1 200 OK\r\nContent-Length: {len("Hello")}\r\nContent-Type: text/plain; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\nHello'.encode()
#         )
#
#
# if __name__ == '__main__':
#     host = "0.0.0.0"
#     port = 8000
#     server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
#     server.serve_forever()
