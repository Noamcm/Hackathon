#Hackathon
import socket
import os
from _thread import *
import time
import scapy.all

def search_two_clients():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1) #(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
    list_of_clients=[1,2]
    #handeling exceptions
    try:    
        message = b"Server started, listening on IP address 172.1.0.4"
        while True:
            server.sendto(message, (socket.gethostbyname(socket.gethostname()), 13117))
            print("message sent!")
            time.sleep(1)
        return(list_of_clients)
    except socket.error as e:
        print("except occurred : " , str(e))


search_two_clients()
#lst= search_two_clients()
#client1=lst[0]
#client2=lst[1]

