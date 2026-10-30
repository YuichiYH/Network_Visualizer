from flask import Blueprint

default_bp = Blueprint('default', __name__)

@default_bp.route('/')
def index():
    return {'message': 'Welcome to the Network Visualizer API'}, 200

@default_bp.route('/health')
def health_check():
    return {'status': 'OK'}, 200