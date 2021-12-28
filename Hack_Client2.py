import socket
import struct
import scapy.all as sc
import sys, errno

my_name = "shiri\n"

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
    return curr_ip,curr_port

def gameMode():
    while True:
        time.sleep(10)

def connecting_to_server(ip,port):
    print("Received offer from "+str(ip)+", attempting to connect...")
    tcp_server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host=socket.gethostbyname(socket.gethostname())
    tcp_server.connect((host,port))
    #tcp_server.bind((host,port))
    tcp_server.sendto(my_name.encode(), (host,port))
    while True:
        try:
            data = str(tcp_server.recv(1024).decode())
            print(data)
            if data.startswith("Welcome"):
                gameMode()
                break
        except OSError as e:
            print(str(e))
            pass
        


#main:
ip,port = search_offer()
connecting_to_server(ip,port)
