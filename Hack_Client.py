import socket
import struct
import scapy.all as sc

'''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(),2068))
message="Client started, listening for offer requests...\n"
client.send(message.encode())#,(serverName, serverPort))
while True:
    from_server = client.recv(4096)
    if not from_server:
        break
    print(from_server.decode("utf-8"))
client.close()
'''
print(sc.get_if_addr('eth1'))
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST , 1)
# Enable broadcasting mode
client.bind(("", 13117))
mreq=struct.pack("4sl", socket.inet_aton(socket.gethostbyname(socket.gethostname())),socket.INADDR_ANY)
client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP , 1)


while True:
    data, addr = client.recvfrom(1024)
    print("received message: %s"%data)
