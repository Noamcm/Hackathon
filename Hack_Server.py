#Hackathon
import socket
import os
from _thread import *
import time
from threading import Thread
import concurrent.futures
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
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #to avoid OSError: [Errno 98] Address already in use
tcp_server.bind((host,port))
player_num=0
players=[]


def main():
    while True: 
        #players=[]
        global player_num
        global players
        tcp_server.listen(2) 
        
        my_threads=[]
        #my_threads.append(Thread(target=search_two_clients, args=()))
        my_threads.append(Thread(target=connect_to_client, daemon=True))
        my_threads.append(Thread(target=connect_to_client, daemon=True))
        for t in my_threads:
            t.start()
        search_two_clients()
        for t in my_threads:
            t.join()
        '''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            futures.append(executor.submit(search_two_clients))
            futures.append(executor.submit(connect_to_client))
            futures.append(executor.submit(connect_to_client))
            for t in concurrent.futures.as_completed(futures):
                print(future.result())
        '''


def connect_to_client():
    global player_num
    global players
    Client, address = tcp_server.accept() 
    packet = Client.recv(1024).decode()
    player_num+=1
    p=Player(player_num,packet,address,Client)
    players.append(p)
    while player_num<2:
        print("waiting for second player...")
        time.sleep(1)
    starts_game(p)

def starts_game(player):
    global players
    time.sleep(3) #10 seconds timer until the game begins
    Player_Message="PLEASE GET OFF THIS PORT!!!!!!!!!!!!!!!!!!!!!\nWelcome to Quick Maths.\n"
    for p in players:
        Player_Message+="Player "+str(p.number)+": "+str(p.name)
    Player_Message+="==\nPlease answer the following question as fast as you can:\nHow much is 2+2?\n"
    player.client.send(Player_Message.encode())
    #add 10 seconds timer for answer
    print("waiting for char....")
    time.sleep(10) #10 seconds timer until the game begins
    answer = player.client.recv(1024).decode()
    print(player.name , answer)


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