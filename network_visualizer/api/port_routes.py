from flask import Blueprint
from network_visualizer.scanner.socket_test import scan_port

port_bp = Blueprint('port', __name__)

@port_bp.route('/scan/<ip>/<port>')
def scan(ip, port):
    result = scan_port(ip, port)
    
    status_code = (
        200
        if result["status"] in ["open", "closed", "filtered"]
        else 400
    )
    
    return result, status_code