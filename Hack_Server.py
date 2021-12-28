#Hackathon
import socket
import os
from _thread import *
import time
import struct
import scapy.all


class Player:
    def __init__(self, number, name, ip):
        self.number = number
        self.name = name
        self.ip = ip


def server_work():
    #while True:
    search_two_clients()



def search_two_clients():
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    host=socket.gethostbyname(socket.gethostname())
    print("Server started, listening on IP address "+str(host))
    port=2068
    tcp_server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket.AF_INET -> ask for protocol IPv4
    # socket.SOCK_STREAM -> ask for TCP connection
    #tcp_server.bind((host,port))
    message = struct.pack('>IbH',0xabcddcba,0x2,port) 
    #Magic cookie (4 bytes): 0xabcddcba
    p_number=1
    lst=[]
    while len(lst)<2:
        udp_server.sendto(message, ('<broadcast>', 13117)) 
        print("message sent!")
        time.sleep(1)
        
        #packet = tcp_server.recvfrom(port) 
        #print(packet)

    


server_work()