
import os
from pathlib import Path
import socket
from http_app import read_request, parse_http_request


PORT = int(os.getenv('PORT', 8080))
SERVER_ERROR_RESPONSE = (f'HTTP/1.1 500 Internal Server Error' + "\n\n" + 'Internal Server Error').encode()
STATIC_FOLDER = Path("./course/webinars/webinar_7/static/")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def file_response(path, protocol):
    with open(STATIC_FOLDER / path, "rb") as fin:
        return f'{protocol} 200 OK\n\n'.encode() + fin.read()


def handle_request(method, path, protocol):
    if method == "OPTIONS":
        return 'HITP/1.1 200 OK' + '\n' + 'Access-Control-Allow-Origin: *'
    
    if method == "GET" and path == "/ping":
        response = f'{protocol} 200 OK' + "\n\n" + 'pong'
        return response.encode()
    
    if method == "GET" and path == "/favicon.ico":
        return file_response("favicon.png", protocol=protocol)
    
    if method == "GET" and path == "/index.html":
        return file_response("index.html", protocol=protocol)
    
    if method == "GET" and path == "/styles.css":
        return file_response("styles.css", protocol=protocol)
    
    response = f'{protocol} 404 Not Found' + "\n\n" + 'Page doesn\'t exists'
    return response.encode()


def run_server():
    try:
        serversocket.bind(("0.0.0.0", PORT))
        serversocket.listen()
        print(f"Start listening at {PORT} port")
        while True:
            client_socket, client_address = serversocket.accept()
            print(f"New connection: {client_address}")
            request = read_request(client_socket)
            print(request)
            try:
                method, path, protocol, _ = parse_http_request(request)
                response = handle_request(method, path, protocol)
            except Exception:
                response = SERVER_ERROR_RESPONSE

            client_socket.sendall(response)
            client_socket.close()

    finally:
        serversocket.close()
        print("Server socket closed...")
    

if __name__ == "__main__":
    run_server()