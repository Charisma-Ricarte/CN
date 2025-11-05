#!/usr/bin/env python3
import socket
import sys
import os
import mimetypes
import threading

# -------------------------------
# Global Connection Tracking
# -------------------------------
lock = threading.Lock()
total_connections = 0
client_connections = {}  # {client_ip: active_count}


def handle_client(connection, client_addr):
    """Serve a single HTTP request from a client, then close the connection."""
    global total_connections, client_connections

    try:
        request = connection.recv(1024).decode()
        if not request:
            return

        print(f"[{client_addr}] Request:\n{request.strip()}\n")

        # Parse request line
        request_line = request.splitlines()[0]
        parts = request_line.split()
        if len(parts) < 3:
            return
        method, path, version = parts

        # Only GET is supported
        if method != 'GET':
            response = "HTTP/1.0 405 Method Not Allowed\r\n"
            response += "Connection: close\r\n\r\n"
            connection.sendall(response.encode())
            return

        # Serve index.html if root is requested
        if path == '/':
            path = '/index.html'

        filepath = '.' + path  # Serve from current directory

        # Handle file not found
        if not os.path.isfile(filepath):
            body = "<html><body><h1>404 Not Found</h1></body></html>"
            response = "HTTP/1.0 404 Not Found\r\n"
            response += "Content-Type: text/html\r\n"
            response += f"Content-Length: {len(body)}\r\n\r\n"
            response += body
            connection.sendall(response.encode())
            return

        # Read and send file
        with open(filepath, 'rb') as f:
            body = f.read()

        mime_type, _ = mimetypes.guess_type(filepath)
        if mime_type is None:
            mime_type = "application/octet-stream"

        header = "HTTP/1.0 200 OK\r\n"
        header += f"Content-Type: {mime_type}\r\n"
        header += f"Content-Length: {len(body)}\r\n"
        header += "Connection: close\r\n\r\n"

        connection.sendall(header.encode() + body)

    except Exception as e:
        print(f"Error handling {client_addr}: {e}")

    finally:
        connection.close()

        # Safely update connection counters
        with lock:
            global total_connections
            total_connections -= 1
            ip = client_addr[0]
            client_connections[ip] -= 1
            if client_connections[ip] <= 0:
                del client_connections[ip]

        print(f"[{client_addr}] Connection closed. Active total: {total_connections}")


def main():
    """Main server loop with concurrency and connection limits."""
    if len(sys.argv) != 7 or sys.argv[1] != '-p' or sys.argv[3] != '-maxclient' or sys.argv[5] != '-maxtotal':
        print("Usage: ./http_server_conc.py -p <port> -maxclient <num> -maxtotal <num>")
        sys.exit(1)

    port = int(sys.argv[2])
    max_client = int(sys.argv[4])
    max_total = int(sys.argv[6])

    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(50)

    print(f"Concurrent HTTP Server running on port {port}")
    print(f"   ▶ Max per client: {max_client}")
    print(f"   ▶ Max total: {max_total}")
    print("   (Press Ctrl+C to stop)\n")

    while True:
        conn, addr = server_socket.accept()
        ip = addr[0]

        with lock:
            current_total = total_connections
            current_client = client_connections.get(ip, 0)

            # Check total connection limit
            if current_total >= max_total:
                msg = "HTTP/1.0 503 Service Unavailable\r\n\r\nToo many total connections"
                conn.sendall(msg.encode())
                conn.close()
                print(f"❌ Refused {addr}: max total connections reached ({max_total})")
                continue

            # Check per-client limit
            if current_client >= max_client:
                msg = "HTTP/1.0 429 Too Many Requests\r\n\r\nToo many connections for this client"
                conn.sendall(msg.encode())
                conn.close()
                print(f"Refused {addr}: client reached limit ({max_client})")
                continue

            # Accept and track connection
            total_connections += 1
            client_connections[ip] = current_client + 1
            print(f"Accepted connection from {addr} | Total: {total_connections}")

        # Spawn a new thread for this connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    main()

