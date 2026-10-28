import asyncio
import socket
import ipaddress

async def async_scan_port(ip, port: int):
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

    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), 
            timeout=5
        )
    except asyncio.TimeoutError:
        return {
            "status": "filtered",
            "message": "Connection attempt timed out.",
            "ip": ip,
            "port": port
        }
    except (ConnectionRefusedError):
        return {
            "status": "closed",
            "message": "Port is closed.",
            "ip": ip,
            "port": port
        }
    else:
        writer.close()
        await writer.wait_closed()
        return {
            "status": "open",
            "message": "Port is open.",
            "ip": ip,
            "port": port
        }


async def async_scan_ip(ip, ports_range_start = 1, ports_range_end = 65535):
    async def worker(port, semaphor):
        async with semaphor:
            return await async_scan_port(ip, port)
    
    tasks = []
    semaphor = asyncio.Semaphore(100)
    
    for port in range(ports_range_start, ports_range_end + 1):
        tasks.append(worker(port, semaphor))
    
    results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    ip = input("Enter the IP address to scan: ")
    
    async_scan_results = asyncio.run(async_scan_ip(ip, 4000, 5024))
    
    closed_ports = [result for result in async_scan_results if result["status"] == "closed"]
    filtered_ports = [result for result in async_scan_results if result["status"] == "filtered"]
    
    for result in async_scan_results:
        if result["status"] in ["closed", "filtered"]:
            continue
        print(f"IP: {result['ip']}, Port: {result['port']}, Status: {result['status']}, Message: {result['message']}")
    print(f"\nTotal closed ports: {len(closed_ports)}")
    print(f"Total filtered ports: {len(filtered_ports)}")