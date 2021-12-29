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
import random


class Player:
    def __init__(self, number, name, address,client):
        self.number = number
        self.name = name
        self.address = address
        self.client = client

def main():
    '''
    this is the main function.
    splits the server to three threads. 
    one of them is responsible for sending broadcast udp packets with the tcp address
    and two of them responsible for communicating with two clients (one for each)
    
    this function will loop as long as the app is running
    '''
    global qa
    try:
        qa = {"How much is 2+2":"4","How much is 0:3":"0","( 2 , 4 , 6 , _ ) -> What comes next":"8"}
        start_print=True
        while True: 
            #players=[] 
            global host,port,udp_server,tcp_server,player_num,players,my_threads,final_Message,has_answer
            host,port,udp_server,tcp_server,player_num,players,my_threads,final_Message,has_answer=init_servers()
            #print("starting main")
            q=get_random_q()
            my_threads.append(Thread(target=search_two_clients,args=(start_print,)))
            my_threads.append(Thread(target=connect_to_client ,args=(q,)))
            my_threads.append(Thread(target=connect_to_client ,args=(q,)))
            for t in my_threads:
                t.start()
            for t in my_threads:
                t.join()
            start_print=False
            close_servers()
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in main")
        return


 
def init_servers():
    '''
    this function is responsible for initiating all the variables for a new game process
    '''
    port=2068
    host=socket.gethostbyname(socket.gethostname())
    try:
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in init_servers - udp_server")
        return
    try:
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #to avoid OSError: [Errno 98] Address already in use
        tcp_server.bind((host,port))
        tcp_server.listen(2) 
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in init_servers - tcp_server")
        return
    player_num=0
    my_threads=[]
    players=[]
    final_Message=""
    has_answer=False
    return(host,port,udp_server,tcp_server,player_num,players,my_threads,final_Message,has_answer)

       

def close_servers():   
    '''
    this function is responsible for closing all the sockets when a game is over
    '''
    try: 
        udp_server.close()
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in closing udp_server")
        return
    try: 
        tcp_server.close()
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in closing tcp_server")
        return


def connect_to_client(q):
    '''for connecting to a client through TCP connection and send and
    this function is responsible receiving player name from the client, waiting for the second cliennt and sending them to the game.
    '''
    try:
        global tcp_server,player_num,players
        Client, address = tcp_server.accept() 
        packet = Client.recv(1024).decode()
        player_num+=1
        p=Player(player_num,packet,address,Client)
        players.append(p)
        while player_num<2:
            #print("waiting for second player...")
            time.sleep(1)
        starts_game(p,q)
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in connect_to_client")
        return

def starts_game(player,q):
    '''
    this function will handle the game.it will send the playes the questions and wait for answer.
    when the forst answer arrive it will announce the player about the winner.
    '''
    global players,final_Message,has_answer
    try:
        time.sleep(3) #10 seconds timer until the game begins
        Player_Message="Welcome to Quick Maths.\n"
        for p in players:
            Player_Message+="Player "+str(p.number)+": "+str(p.name)
        Player_Message+="==\nPlease answer the following question as fast as you can:\n"+q+"?\n"
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in starts_game")
        return
    try:
        player.client.send(Player_Message.encode())
    except IOError as er:
        if er.errno == errno.EPIPE:
            print("recieved error: (" + str(er) + ") in communicating with tcp server")
        return
    try:
        readable, empty, empt = select.select([player.client], [], [] , 10 ) # wait just 5sec 
        print(has_answer)
        print(readable)
        if not readable and not has_answer:
            final_Message="\nGame over!\nThe correct answer was "+qa.get(q)+"!\nThe game finished with a DRAW\n"
        elif not has_answer:
            has_answer=True
            client = readable[0]
            answer = client.recv(1024).decode()
            #print(player.name,answer)
            if (answer==qa.get(q)):
                final_Message="\nGame over!\nThe correct answer was "+qa.get(q)+"!\nnCongratulations to the winner: "+player.name
            else:
                other_player = ""
                for p in players:
                    if p.name!=player.name:
                        other_player = p.name
                final_Message="\nGame over!\nThe correct answer was "+qa.get(q)+"!\nCongratulations to the winner: "+ other_player

    except socket.error as er:
        print("recieved error: (" + str(er) + ") in starts_game")
        return
    try:
        player.client.send(final_Message.encode())
    except IOError as er:
        if er.errno == errno.EPIPE:
            print("recieved error: (" + str(er) + ") in communicating with tcp server")
        return

def search_two_clients(boolean):
    '''
    this function is responsible for sending UDP packets through the udp server until there will be 2 players.
    '''
    global host,port,udp_server,player_num
    try:
        if boolean:
            print("Server started, listening on IP address "+str(host))
        else:
            print("Game over, sending out offer requests...")
        # socket.AF_INET -> ask for protocol IPv4
        # socket.SOCK_STREAM -> ask for TCP connection
        message = struct.pack('>IbH',0xabcddcba,0x2,port)  #Magic cookie (4 bytes): 0xabcddcba
        while player_num<2: #TO CHANGE
            udp_server.sendto(message, ('<broadcast>', 13117)) 
            #print("message sent!")
            time.sleep(1)
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in search_two_clients")
        return

def get_random_q():
    global qa
    random_num = random.randint(0,len(qa.keys())-1)
    random_key = list(qa.keys())[random_num]
    return str(random_key)

main()