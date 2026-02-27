import socket
from datetime import datetime

def run_honeypot(port=80):
    banner = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Management Login</h1></body></html>"
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)
        
        print(f"--- SOVEREIGN HONEYPOT ACTIVE ---")
        print(f"[*] Listening on Port: {port}")
        
        while True:
            client_conn, client_addr = server_socket.accept()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Receive data
            data = client_conn.recv(1024).decode('utf-8', errors='ignore')
            
            # --- NEW LOGIC: Extract True IP from Headers ---
            true_ip = client_addr[0] # Default to the immediate connection
            for line in data.splitlines():
                if line.startswith("X-Forwarded-For:"):
                    # The format is "X-Forwarded-For: 1.2.3.4"
                    true_ip = line.split(":")[1].strip()
                    break
            # -----------------------------------------------

            print(f"\n[!!!] ALERT: SNOOP DETECTED [!!!]")
            print(f"TIME: {timestamp}")
            print(f"DIRECT SOURCE (Proxy): {client_addr[0]}")
            print(f"HIDDEN SOURCE (True IP): {true_ip}") # This reveals the bot/attacker
            print(f"SOURCE PORT: {client_addr[1]}")
            print(f"DATA EXTRACTED:\n{data}")
            
            client_conn.send(banner.encode('utf-8'))
            client_conn.close()
            print("-" * 40)
            
    except Exception as e:
        print(f"System Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_honeypot(port=8080)
