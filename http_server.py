#!/usr/bin/env python3
import socket
import sys
import os
import mimetypes

def handle_client(connection):
    request = connection.recv(1024).decode()
    print("Received request:\n", request)

    if not request:
        return

    # Parse the first line of the request
    request_line = request.splitlines()[0]
    parts = request_line.split()
    if len(parts) < 3:
        return
    method, path, version = parts

    if method != 'GET':
        response = "HTTP/1.0 405 Method Not Allowed\r\n\r\n"
        connection.sendall(response.encode())
        return

    # Default to index.html if root is requested
    if path == '/':
        path = '/index.html'

    filepath = '.' + path  # Serve files from current directory

    if not os.path.isfile(filepath):
        body = "<html><body><h1>404 Not Found</h1></body></html>"
        response = "HTTP/1.0 404 Not Found\r\n"
        response += "Content-Type: text/html\r\n"
        response += f"Content-Length: {len(body)}\r\n\r\n"
        response += body
        connection.sendall(response.encode())
        return

    with open(filepath, 'rb') as f:
        body = f.read()

    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type is None:
        mime_type = "application/octet-stream"

    header = "HTTP/1.0 200 OK\r\n"
    header += f"Content-Type: {mime_type}\r\n"
    header += f"Content-Length: {len(body)}\r\n\r\n"

    print("📤 Sending response headers:\n", header)
    connection.sendall(header.encode() + body)


def main():
    if len(sys.argv) != 3 or sys.argv[1] != '-p':
        print("Usage: ./http_server.py -p <port>")
        sys.exit(1)

    port = int(sys.argv[2])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)

    print(f"Serving HTTP on port {port} ... (Press Ctrl+C to stop)")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(conn)
        conn.close()

if __name__ == '__main__':
    main()
