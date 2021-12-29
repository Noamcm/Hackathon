import socket
import struct
import scapy.all as sc
import sys, errno
from getch import getch, getche


my_name = "Shiri\n"


def search_offer():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s.bind(('',13117))
    print("Client started, listening for offer requests...")
    curr_port=0
    curr_ip=0
    while curr_port!=2068: #True: ???
        try:
            packet = s.recvfrom(13117)  
            if str(packet[0]).startswith(r"b'\xab\xcd\xdc\xba\x02"):
                unpacked = struct.unpack('>IbH',packet[0])
                curr_port=unpacked[2]
                curr_ip=packet[1][0]
        except struct.error as e:
            print("recieved error: ("+str(e)+") from port: " +str(curr_port) ) ##?????????
            continue
    connecting_to_server(curr_ip,curr_port)

def connecting_to_server(ip,port):
    print("Received offer from "+str(ip)+", attempting to connect...")
    tcp_server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host=socket.gethostbyname(socket.gethostname())
    tcp_server.connect((host,port))
    tcp_server.sendto(my_name.encode(), (host,port))
    while True:
        try:
            data = str(tcp_server.recv(1024).decode())
            print(data)
            if data.startswith("Welcome"):
                gameMode(tcp_server)
                break
        except OSError as e:
            print(str(e))
            pass
        
def gameMode(tcp_server):
    char = getche()
    tcp_server.sendto(char.encode(),tcp_server.getpeername())
    data = str(tcp_server.recv(1024).decode())
    print(data)



#main:
search_offer()
