import json
import socket
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app, resources={r'/*': {"origins": '*'}})

#RCON
def rcon(ip, port, password, command):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.8)
        sock.connect((ip, int(port)))

        sock.send(b"\xFF\xFF\xFF\xFF\x02rcon " + str.encode(password) + b" " + str.encode(command))
        received = sock.recv(65565)
        return received
        sock.close()

#Handle RCON requests
@app.route('/rcon',methods=['GET', 'POST'])
@cross_origin(allow_headers=['Content-Type'])
def handle_req():
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json()
        result = rcon(data["ip"], data["port"], data["password"], data["command"])
        test = result.replace(b'\xff\xff\xff\xff\x01', b'')
        bytesToJson = test.decode('utf8')
        resultSplitted = bytesToJson.splitlines()
        r = make_response(json.dumps(resultSplitted))
        r.mimetype = 'application/json'
        return r
    else:
        return json.dumps({'error': { "code": 415, "message": "Media Type not supported."} })



#Main URI
@app.route('/')
@cross_origin(allow_headers=['Content-Type'])
def main():
        return "Choo choo, nothing to see here!"


if __name__ == '__main__':
    app.run(threaded=True,debug=False,use_evalex=False,host='0.0.0.0')
