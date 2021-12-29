#Hackathon
import socket
import os
from _thread import *
import time
from threading import Thread
import concurrent.futures
import select
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
final_Message=""
has_answer=False

def main():
    while True: 
        #players=[]
        global player_num
        global players   
        my_threads=[]
        tcp_server.listen(2) 
        print("starting main")
        my_threads.append(Thread(target=connect_to_client, daemon=True))
        my_threads.append(Thread(target=connect_to_client, daemon=True))
        for t in my_threads:
            t.start()
        search_two_clients()
        for t in my_threads:
            t.join()
        

def connect_to_client():
    global player_num
    global players
    Client, address = tcp_server.accept() 
    packet = Client.recv(1024).decode()
    player_num+=1
    p=Player(player_num,packet,address,Client)
    players.append(p)
    while player_num<2:
        #print("waiting for second player...")
        time.sleep(1)
    starts_game(p)

def starts_game(player):
    global players
    global final_Message
    global has_answer
    time.sleep(3) #10 seconds timer until the game begins
    Player_Message="Welcome to Quick Maths.\n"
    for p in players:
        Player_Message+="Player "+str(p.number)+": "+str(p.name)
    Player_Message+="==\nPlease answer the following question as fast as you can:\nHow much is 2+2?\n"
    player.client.send(Player_Message.encode())
    #add 10 seconds timer for answer
    #print("waiting for char....")
    #time.sleep(10) #10 seconds timer until the game begins
    readable, empty, empt = select.select([player.client], [], [] , 5 ) # wait just 5sec 
    if not readable and not has_answer:
        final_Message="Game over!\nThe correct answer was "+answer+"!\nThe game finished with a DRAW\n"
    elif not has_answer:
        has_answer=True
        client = readable[0]
        answer = client.recv(1024).decode()
        print(player.name,answer)
        if (answer=="4"):
            final_Message="Game over!\nThe correct answer was "+answer+"!\nnCongratulations to the winner: "+player.name
        else:
            other_player = ""
            for p in players:
                if p.name!=player.name:
                    other_player = p.name
            final_Message="Game over!\nThe correct answer was "+answer+"!\nCongratulations to the winner: "+ other_player
    player.client.send(final_Message.encode())

'''
def timer():
    global my_threads
    while player_num<2:
        time.sleep(1)
    while player_num==2:
        print("in while 1")
        time.sleep(5) #the game
        #now 10 sec is over
        print("GAME OVER")
        for t in my_threads:
            t.stop()

'''

def search_two_clients():
    global player_num
    timeout = time.time() + 60*2   # 5 minutes from now
    print("Server started, listening on IP address "+str(host))
    # socket.AF_INET -> ask for protocol IPv4
    # socket.SOCK_STREAM -> ask for TCP connection
    message = struct.pack('>IbH',0xabcddcba,0x2,port)  #Magic cookie (4 bytes): 0xabcddcba
    while player_num<2: #TO CHANGE
        udp_server.sendto(message, ('<broadcast>', 13117)) 
        #print("message sent!")
        time.sleep(1)

main()