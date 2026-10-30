from flask import Flask
from network_visualizer.api import api_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app
