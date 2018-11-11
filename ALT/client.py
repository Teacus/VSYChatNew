# -*- coding: cp1252 -*-
# created by Tobias Jülg 28.11.2015
# client

# imports:
import socket
from threading import Thread
from time import sleep
import os

# Konstanten:
global host_ip
host_ip = "192.168.2.52"

global port
port = 20997

# name welcher im chat angezeigt wird
global name
name = "Jobi"


##############################################################
# Server_connection:
##############################################################

class server_connection(Thread):

    def __init__(self, ip, Port):
        self.ip = ip
        self.port = Port

        print("(Client)" + 'TO: IP: ' + self.ip + '\n(Client)port: ' + str(self.port))

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket Objekt
            self.server.connect((str(self.ip), int(self.port)))  # verbungsaufbau zum Server
            print("(Client)" + "connected")

            # handshake
            self.server.sendall(b'Chat_certified_client')
            got = self.recv()
            print(got)

            if got == "full":
                print("(Client)" + "Server is full")
                self.close()

            elif got == "ok":
                print("(Client)" + "sucessfull handshake")
                Thread.__init__(self)
                self.start()
                self.inputSender()

            else:
                print("(Client)" + "unexpected Welcome msg")
                #self.close()


        # falls die Verbindung abreißt oder keine möglich ist
        except socket.error:
            print("(Client)" + "Server is not online or wrong certificate")
            self.close()

    # schließt die Verbindung zum Server und beendet den Client
    def close(self):
        self.server.close()
        print("(Client)" + "PROGRAMM WIRD GESCHLOSSEN!")
        sleep(1)
        os._exit(1)

    # sendet text an den Server
    def send(self, text):
        self.server.sendall(text)

    # ließt den buffer auf neue strings vom server, es wird gewartet falls er leer ist
    def recv(self):
        return self.server.recv(1024)

    # Thread: warte auf neue strings vom server und printe sie
    def run(self):
        while True:
            try:
                text = self.recv()
                print("(Chat) " + text)

            except socket.error:
                print("(Client)" + "Server closed")
                self.close()

    # wartet auf einen input und schickt diesen an den server
    def inputSender(self):
        self.send(name + " joined the room")
        while True:
            try:
                toSend = raw_input("")
                if toSend != "":
                    print("(Chat) You: " + str(toSend))
                    self.send(name + ": " + str(toSend))

            except KeyboardInterrupt:
                print("(Client)" + "Close..")
                self.send(name + " left the room")
                self.close()

            except socket.error:
                print("(Client)" + "Server closed")
                self.close()


if __name__ == "__main__":
    server_connection(host_ip, port)