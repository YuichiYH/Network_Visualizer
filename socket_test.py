import socket
import ipaddress

def scan_port(ip, port: int):
    
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid IP address.",
            "ip": ip,
            "port": port
        }
    
    if not isinstance(port, int):
        return {
            "status": "error",
            "message": "Port number must be an integer.",
            "ip": ip,
            "port": port
        }
    
    if port < 1 or port > 65535:
        return {
            "status": "error",
            "message": "Port number must be between 1 and 65535.",
            "ip": ip,
            "port": port
        }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(5)
        error = client.connect_ex((ip, port))
        
        if error == 0:
            return {
                "status": "open",
                "ip": ip,
                "port": port
            }

        else:
            match error:
                case socket.errno.ECONNREFUSED:
                    return {
                        "status": "closed",
                        "ip": ip,
                        "port": port
                    }
                case socket.errno.ETIMEDOUT:
                    return {
                        "status": "filtered",
                        "ip": ip,
                        "port": port
                    }
                case _:
                    return {
                        "status": "unreachable",
                        "ip": ip,
                        "port": port
                    }

if __name__ == "__main__":
    ip = input("Enter the IP address to scan: ")
    port = int(input("Enter the port number to scan: "))
    
    result = scan_port(ip, port)
    print(result)