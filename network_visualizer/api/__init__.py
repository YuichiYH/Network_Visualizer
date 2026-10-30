from flask import Blueprint

api_bp = Blueprint('api', __name__)

from network_visualizer.api.default_routes import default_bp
from network_visualizer.api.port_routes import port_bp

api_bp.register_blueprint(default_bp)
api_bp.register_blueprint(port_bp)
