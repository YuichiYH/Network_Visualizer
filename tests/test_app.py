from urllib import response

import pytest
import socket
from network_visualizer.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client
        
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Welcome to the Network Visualizer API'}

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'OK'}
    
def test_scan_open_port(client):
    ip = "127.0.0.1"
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((ip, 0))
        server.listen(1)
        
        port = server.getsockname()[1]
    
        response = client.get(f'/scan/{ip}/{port}')
        assert response.status_code == 200
        assert response.json["status"] == "open"
        
def test_scan_closed_port(client):
    ip = "127.0.0.1"
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((ip, 0))
        server.listen(1)
        
        port = server.getsockname()[1]
        server.close()
    
        response = client.get(f'/scan/{ip}/{port}')
        assert response.status_code == 200
        assert response.json["status"] == "closed"
        
def test_scan_invalid_ip(client):
    ip = "999.1.1.1"
    port = 80
    
    response = client.get(f'/scan/{ip}/{port}')
    assert response.status_code == 400
    assert response.json["status"] == "error"
    assert response.json["message"] == "Invalid IP address."
    
def test_scan_invalid_port(client):
    ip = "127.0.0.1"
    port = "123a"
    
    response = client.get(f'/scan/{ip}/{port}')
    assert response.status_code == 400
    assert response.json["status"] == "error"
    assert response.json["message"] == "Port number must be an integer."