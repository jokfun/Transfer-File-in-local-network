"""
    TODO : 
    - made a GUI of the app
    - add a progressbar during the process
    - make threads for multiple transfer
"""

import socket
import sys
import tqdm
import os
from random import randint

#Get the adress of the computer and a new port
hostname = socket.gethostname()    
ADRESS = socket.gethostbyname(hostname)
PORT = randint(1000,9999)

def askFile():
    """
        Ask a file to the other computer
    """
    print("\n-- Ask a file --")

    #Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Ask the user to enter the ids of the target computer
    ipadress = input("Enter the ip adress : ")
    port = input("Enter the port : ")
    try:
        s.connect((ipadress, int(port)))
    except Exception as e:
        print("Incorrect Connection.")
        return None

    #Ask the user the password of the target for this session
    password = input("Connection password : ")
    s.send(password.encode())
    result =  s.recv(1024).decode()

    #If the password is not correct, return to the main menu
    if result != "ok":
        print("Wrong password.")
        return 0

    #Ask the path of the file the user want to download
    fileName = input("Name of the file : ")

    s.send(fileName.encode())

    message =  s.recv(1024).decode()

    #If the file doesn't exist, return to the main menu
    if message!="File found.":
        print(message)
        return None

    #Change the path in order to keep the name and the extansion of the file
    fileName = fileName.split("/")[-1].split("\\")[-1]

    #Start the transfer
    print("Receiving file...")

    #If the transfer is a failure, the app will not crash
    try:
        f = open("copy_"+fileName,'wb')
        content = s.recv(1024)
        while content:
            f.write(content)
            content = s.recv(1024)
    except Exception as e:
        print(e)
        print("Reception of the file cancelled.")
        return None


def sendFile():
    """
        Send a file to a user
    """

    print("\n--Send a file--")

    #Create a password for the session
    password = str(randint(10000,99999))
    print("Session password :",password)

    #Create an input socket
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((ADRESS,PORT))

    #Allow only one computer to connect to the server
    tcpsock.listen(1)

    #Accept the new connection
    (clientsocket, (ip, port)) = tcpsock.accept()

    #test if the password is correct
    r = clientsocket.recv(1024).decode()
    if r == password:
        clientsocket.send("ok".encode("ascii"))
    else:
        clientsocket.send("error".encode("ascii"))
        return None

    #Receive the path of the file
    path_file = clientsocket.recv(1024).decode().split("\n")[0]

    #test if the path of the file is correct
    try:
        f = open(path_file,"rb")
        clientsocket.send("File found.".encode("ascii"))
    except Exception as e:
        clientsocket.send("Error while loading the file.".encode("ascii"))
        return None

    #Start the transmission of the file
    print("File transmission...")

    #If an exception is raised, wil lreturn an error
    try:
        file = f.read(1024)
        while file:
            clientsocket.send(file)
            file = f.read(1024)
        f.close()
        terminated = True
    except Exception as e:
        print(e)
        print("Transmission of the file cancelled.")
        return None

def main():

    #init the var request for the user
    request = "" 

    #Print the ip and the port of the session, 
    #will be usefull the one who want the file 
    print("Your ip adress is :",ADRESS)
    print('Session PORT is :', PORT)

    #Global loop
    #As long as the user doesn't want to leave the app
    while request != "q":
        #List of possibilities
        print("\nCode : \ns : send a file\nr : receive a file\nq : leave the app")
        #Update the request
        request = input("Choice : ")
        if request == "s":
            sendFile()
        if request == "r":
            askFile()

if __name__ == "__main__":
    main()

