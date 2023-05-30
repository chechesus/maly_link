import socket
import json
import hashlib
from urllib.parse import urlparse

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 80

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

def response_index(response:str):
    # request na stranku pre html
    with open("index.html") as reader:
        response += "Content-Type: text/html; charset=UTF-8`\n\n"
        response += reader.read()
    return response

url_map = {}

def shorten_url(request, response):
    try:
        print("Request:", request)
        body = request.split("\n\n")
        if len(body) < 2:
            body = request.split("\r\n\r\n")
        print("Body:", body)
        data = json.loads(str(body[1]))
        print("Data:", data)
        long_url = data["longUrl"]

        # Hash generation 
        h = hashlib.new('sha256')
        h.update(long_url.encode()) # String to hash 
        short_url = h.hexdigest()[:8]

        # Original URL into map 
        url_map[short_url] = long_url

        response_data = {"shortUrl": "http://localhost/" + short_url}
        response_data_str = json.dumps(response_data)
        response += "Content-Type: application/json; charset=UTF-8\n"
        response += "Content-Length: " + str(len(response_data_str)) + "\n\n"
        response += response_data_str
    except Exception as e:
        print("ERROR:", e)
        raise
        
    return response

while True:    
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(4096).decode()
    print(request)

    try:
        lines = request.split("\n")
        req, path, http_ver = lines[0].split(" ")
        print("req:", req, "path:", path, "ver:", http_ver)
        print("CESTA:", path)
    except:
        break
    response = 'HTTP/1.1 200 OK\n' 

    # Function routing
    if req == "GET" and (path == "/"  or path == "/index.html"):
        response = response_index(response)
    elif req == "POST":
        print("reading body")
        request += client_connection.recv(4096).decode()
        response = shorten_url(request, response)
    else:
        # Handle other request methods
        parsed_url = urlparse(path)

        # Parse the slash
        short_url = parsed_url.path[1:]

        if short_url in url_map:
             long_url = url_map[short_url]
             response = 'HTTP/1.1 307 Temporary Redirect\n'# Temporarely redirected message
             response += f"Location: {long_url}\n\n" #Redirects to original URL

    # Send HTTP response
    print("RESPONSE:", response)
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()