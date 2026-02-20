import socket
from datetime import datetime

def run_honeypot(port=80, banner="HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body><h1>Management Login</h1><form>User: <input type='text'><br>Pass: <input type='password'></form></body></html>"):
    # Create a "Sovereign" Socket
    # AF_INET = IPv4, SOCK_STREAM = TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bind to all interfaces on the chosen port
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)
        
        print(f"--- SOVEREIGN HONEYPOT ACTIVE ---")
        print(f"[*] Listening for snoops on Port: {port}")
        print(f"[*] Waiting for a 'Savage' signal...")
        
        while True:
            # Wait for someone to "touch" the trap
            client_conn, client_addr = server_socket.accept()
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[!!!] ALERT: SNOOP DETECTED [!!!]")
            print(f"TIME: {timestamp}")
            print(f"SOURCE IP: {client_addr[0]}")
            print(f"SOURCE PORT: {client_addr[1]}")
            
            # Receive the "Attack" data (the scan or the request)
            data = client_conn.recv(1024).decode('utf-8', errors='ignore')
            print(f"DATA EXTRACTED:\n{data}")
            
            # Send the "Bait" back to the snoop to keep them occupied
            client_conn.send(banner.encode('utf-8'))
            client_conn.close()
            
            print("-" * 40)
            
    except Exception as e:
        print(f"System Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    # You can change the port to 23 (Telnet) or 8080 (Common Web)
    run_honeypot(port=8080)