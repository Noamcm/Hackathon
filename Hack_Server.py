#Hackathon
import socket
import os
from _thread import *
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import struct
import scapy.all


class Player:
    def __init__(self, number, name, address,client):
        self.number = number
        self.name = name
        self.address = address
        self.client = client

port=2068
host=socket.gethostbyname(socket.gethostname())
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((host,port))
player_num=0

def main():
    while True: 
        #players=[]
        global player_num
        tcp_server.listen(2) 
        my_threads=[]
        my_threads.append(threading.Thread(target=search_two_clients, args=()))
        my_threads.append(threading.Thread(target=connect_to_client, args=()))
        my_threads.append(threading.Thread(target=connect_to_client, args=()))
        for t in my_threads:
            t.start()
        for t in my_threads:
            t.join()
    


def connect_to_client():
    global player_num
    print("after listen")
    Client, address = tcp_server.accept() 
    packet = Client.recv(1024).decode()
    player_num+=1
    p=Player(player_num,packet,address,Client)
    #players.append(p)
    welcome_Message="Welcome to Quick Maths.\n"
    Client.send(welcome_Message.encode()) #only if two clients! #TODO check!
    time.sleep(10)
    starts_game(p)

def starts_game(player):
    print("Player "+str(player.number)+": "+str(player.name))
    time.sleep(3)


def search_two_clients():
    global player_num
    timeout = time.time() + 60*2   # 5 minutes from now
    print("Server started, listening on IP address "+str(host))
    # socket.AF_INET -> ask for protocol IPv4
    # socket.SOCK_STREAM -> ask for TCP connection
    #tcp_server.bind((host,port))
    message = struct.pack('>IbH',0xabcddcba,0x2,port) 
    #Magic cookie (4 bytes): 0xabcddcba
    while player_num<2: #TO CHANGE
        udp_server.sendto(message, ('<broadcast>', 13117)) 
        #print("message sent!")
        time.sleep(1)


main()