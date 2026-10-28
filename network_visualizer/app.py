import ipaddress
from flask import Flask
from network_visualizer.scanner.socket_test import scan_port

app = Flask(__name__)

@app.route('/')
def index():
    return {'message': 'Welcome to the Network Visualizer API'}, 200

@app.route('/health')
def health_check():
    return {'status': 'OK'}, 200

@app.route('/scan/<ip>/<port>')
def scan(ip, port):
    result = scan_port(ip, port)
    
    status_code = (
        200
        if result["status"] in ["open", "closed", "filtered"]
        else 400
    )
    
    return result, status_code