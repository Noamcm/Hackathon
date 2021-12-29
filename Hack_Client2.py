import socket
import struct
import scapy.all as sc
import sys, errno
from getch import getch, getche

my_name = "Shiri\n"

def search_offer():
    #this function searches for server's offer
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.bind(('',13117))
        print("Client started, listening for offer requests...")
        curr_port=0
        curr_ip=0
        while curr_port!=2068: #True: ???
            try:
                packet = s.recvfrom(13117)  #recieve an offer
                if str(packet[0]).startswith(r"b'\xab\xcd\xdc\xba\x02"): #checks Magic Cookie and Message type prefix
                    unpacked = struct.unpack('>IbH',packet[0])
                    curr_port=unpacked[2]
                    curr_ip=packet[1][0]
            except struct.error as e:
                print("recieved error: ("+str(e)+") from port: " +str(curr_port) ) ##?????????
                continue
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in search offer")
        return
    connecting_to_server(curr_ip,curr_port) #connect to tcp...

def connecting_to_server(ip,port):
    #this function connects the client and the server with TCP connection
    print("Received offer from "+str(ip)+", attempting to connect...")
    try:
        tcp_server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host=socket.gethostbyname(socket.gethostname())
        tcp_server.connect((host,port))
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in connecting to tcp server")
        return
    try:
        tcp_server.sendto(my_name.encode(), (host,port)) #send client's name to the server 
    except IOError as er:
        if er.errno == errno.EPIPE:
            print("recieved error: (" + str(er) + ") in sending data to server with tcp server")
        return
    try:
        data = str(tcp_server.recv(1024).decode()) #recieve welcome to game message
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in recieving data from server with tcp server")
        return
    print(data)
    if data.startswith("Welcome"): 
        gameMode(tcp_server) #start game...
        
def gameMode(tcp_server):
    #this function contains the fuctionality of the client's game mode
    char = getche() #get the first char that was written, without enter being pressed
    try:
        tcp_server.sendto(char.encode(),tcp_server.getpeername()) #send the answer to the server
    except IOError as er:
        if er.errno == errno.EPIPE:
            print("recieved error: (" + str(er) + ") in sending data to server in game mode")
    try:
        data = str(tcp_server.recv(1024).decode()) #get server's results of the game
    except socket.error as er:
        print("recieved error: (" + str(er) + ") in recieving data from server in game mode")
        return
    print(data)
    print("Server disconnected, listening for offer requests...")

#main:
while True: #so the client will get more offers after finishing a game with a server
    search_offer()