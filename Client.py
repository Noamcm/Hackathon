import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(),2068))
message="Client started, listening for offer requests...\n"
client.send(message.encode())#,(serverName, serverPort))
while True:
    from_server = client.recv(4096)
    print(from_server.decode("utf-8"))
client.close()