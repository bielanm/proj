

CHUNK_SIZE = 256
BREAK_LINE = "\r\n"
HTTP_BREAKS = ["\n\n", BREAK_LINE*2]


def read_request(client_socket):
    chunks = []
    while True:
        request = client_socket.recv(CHUNK_SIZE).decode()
        chunks.append(request)
        if any(request.endswith(end) for end in HTTP_BREAKS) or (not request):
            break
    
    request = "".join(chunks)
    return request


def parse_http_request(request):
    request_header, headers = request.split(BREAK_LINE, 1)
    method, path, protocol = request_header.split()
    
    parsed_headers = {}
    for header in headers.split(BREAK_LINE):
        if not header:
            continue
        header_name, header_value = header.split(":", 1)
        parsed_headers[header_name.strip()] = header_value.strip()
    
    return method, path, protocol, parsed_headers
