import pytest
import socket
from socket_test import scan_port

def test_scan_port_rejects_invalid_ip():
    ip = "999.1.1.1"
    port = 80
    
    result = scan_port(ip, port)
    assert result["status"] == "error"
    assert result["message"] == "Invalid IP address."

def test_scan_ip_and_port_invalid():
    ip = "invalid_ip"
    port = 80000
    
    result = scan_port(ip, port)
    assert result["status"] == "error"
    assert result["message"] == "Invalid IP address."
    
def test_scan_port_rejects_zero():
    ip = "127.0.0.1"
    port = 0
    
    result = scan_port(ip, port)
    assert result["status"] == "error"
    assert result["message"] == "Port number must be between 1 and 65535."
        
def test_scan_port_rejects_65536():
    ip = "127.0.0.1"
    port = 65536
    
    result = scan_port(ip, port)
    assert result["status"] == "error"
    assert result["message"] == "Port number must be between 1 and 65535."

def test_scan_port_rejects_non_integer():
    ip = "127.0.0.1"
    port = "not_an_integer"
    
    result = scan_port(ip, port)
    assert result["status"] == "error"
    assert result["message"] == "Port number must be an integer."


def test_scan_port_closed_port():
    ip = "127.0.0.1"
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((ip, 0))
        server.listen(1)
        
        port = server.getsockname()[1]
        server.close()
    
    result = scan_port(ip, port)
    assert result["status"] == "closed"

def test_scan_port_open_port():
    ip = "127.0.0.1"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((ip, 0))
        server.listen(1)
        
        port = server.getsockname()[1]
        
        result = scan_port(ip, port)
        assert result["status"] == "open"