#Hackathon
import socket
import os
from _thread import *
import scapy.all


serv= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET -> ask for protocol IPv4
# socket.SOCK_STREAM -> ask for TCP connection


#my_ip = scapy.get_if_
ThreadCount = 0

#handeling exceptions
try:    
    
    IP_add=socket.gethostbyname(socket.gethostname())
    serv.bind((socket.gethostname(),2068))  #2068 our port
    print(f"Server started, listening on IP address {IP_add} ")
    serv.listen(5) #only for two clients ?
    '''
    while True: 
        clientsocket1, address1 = serv.accept() 
        print(f"connection from {address1} has been established!")
        welcome_Message="Welcome to Quick Maths.\n"
        clientsocket1.send(welcome_Message.encode()) #only if two clients! #TODO check!
        from_client1 =''
        while True:
            data1=clientsocket1.recv(4096)
            if not data1: break
            from_client1+= data1.decode("utf-8")
            print(from_client1)
            message = "I am Server\n"
            clientsocket1.send(message.encode())
        print('client disconnected')
        break
    '''
    def start_game(connection):
        connection.send("Welcome to Quick Maths.\n".encode())
        while True:
            try:  
                data = connection.recv(4096)
                reply = 'Server Says: ' + data.decode('utf-8')
                if not data:
                    break
                connection.sendall(str.encode(reply))  
            except socket.error as e:
                print(str(e))
                break
        print('client disconnected')
        

    while True:
        
        Client, address = serv.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        #start_game, (Client, )
        start_new_thread(start_game, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        #break


except socket.error as e:
    print("cheeckkiiinnnnggg " , str(e))





