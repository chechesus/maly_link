import socket
import json


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

def shorten_url(request, response):
    try:
        # body = request.split("\n\n")[1]
        # data = json.loads(body)
        # print(data)
        print(request)
        response_data = {"shortUrl":""}
        response_data_str = json.dumps(response_data)
        response += "Content-Type: application/json; charset=UTF-8\n"
        response += "Content-Length: "+str(len(response_data_str))+"\n\n"
        response += response_data_str
    except Exception as e:
        print("ERROR:", e)
        print(request)
        pass

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()
    # print(client_address)
    # Get the client request
    request = client_connection.recv(4096).decode()
    # print(request)

    try:
        lines = request.split("\n")
        # print(request)
        req, path, http_ver = lines[0].split(" ")
        print("req:", req, "path:", path, "ver:", http_ver)
    except:
        break
    response = 'HTTP/1.1 200 OK\n' 

    
    # function routing
    if req == "GET" and (path == "/"  or path == "/index.html"):
        response = response_index(response)
    elif req == "POST":
        response = shorten_url(request, response)

    # Send HTTP response
    print("RESPONSE:", response)
    client_connection.sendall(response.encode())
    client_connection.close()



# Close socket
server_socket.close()