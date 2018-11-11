# -*- coding: utf-8 -*-
# created by Tobias Jülg 28.11.2015
# server

# imports
import socket
from threading import Thread
from time import sleep
import os

# Konstanten:
global slots
slots = 5

global host_ip
host_ip = socket.gethostbyname(socket.gethostname())

global port
port = 20997


class socketServer:
    "Klasse, welche den Server erstellt und nach Clienten lauscht"

    def __init__(self, ip, Port):
        "erstellt die Arrays mit größe 'slots' größe"
        self.clients = [0 for x in range(slots)]
        self.addr = [0 for x in range(slots)]
        self.slot = [0 for x in range(slots)]
        self.clients_rev = [0 for x in range(slots)]

        for i in range(len(self.slot)):
            self.slot[i] = 0

        self.host = ip
        self.port = Port

        print("SocketServer - IP: " + ip)
        print("SocketServer - PORT: " + str(Port))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host_ip, port))

        print("SocketServer - " + str(slots) + " slots")
        print("SocketServer - " + "Waiting for clients...")

        self.listenForClients()  # start listening

    def listenForClients(self):
        "Schleife welche nach Clients lauscht, für jeden neuen Client wird die Klasse connected geöffnet"

        try:
            while True:

                self.sock.listen(1)
                client, addr = self.sock.accept()

                for i in range(len(self.slot)):
                    if self.slot[i] == 0:
                        self.slot[i] = 1
                        test = True
                        break
                    else:
                        test = False
                if test == True:
                    self.clients[i] = client
                    self.addr[i] = addr

                    self.clients_rev[i] = connected(self, i)

                    print("SocketServer - " + str(i + 1) + "/" + str(slots) + " clients connected")
                else:
                    print("SocketServer - Server is full")
                    client.send(b'full')
                    client.close()

        except KeyboardInterrupt:
            self.shutServerDown()
            print("SocketServer - " + "Server shutdown")
            sleep(1)
            os._exit(1)

    def shutServerDown(self):
        "schließt alle aktuellen Verbindungen"
        self.Listening = False
        for i in range(len(self.clients)):
            if self.slot[i] == 1 and self.clients[i] != None and self.clients[i] != 0:
                self.clients[i].close()


class connected(Thread):
    "Für jeden neuen Client wird ein neues Objekt dieser Klasse erzeugt"

    def __init__(self, sockt, num):
        "Startet einen neuen Thread"
        self.num = num
        self.sockt = sockt
        print("SocketServer - " + 'Connected with ' + str(self.sockt.addr[self.num]))

        Thread.__init__(self)
        self.start()

    def closeClient(self):
        "schließt den Client und gibt den Slot frei"
        print("SocketServer - " + str(self.sockt.addr[self.num]) + " disconnected")
        print("SocketServer - " + "Slot " + str(self.num) + " is now available")
        self.sockt.slot[self.num] = 0
        self.sockt.clients[self.num].close()
        self.sockt.clients[self.num] = None

    def send(self, text):
        "sendet den 'text' an den Client"
        self.sockt.clients[self.num].sendall(text)  # ggf mit \n

    def recv(self):
        "gibt den Inhalt des Buffers zurück, falls nichts im Buffer steht wartet der Interpreter an dieser Stelle"
        return self.sockt.clients[self.num].recv(1024)

    def run(self):
        "Handshake und weiterleitung der ankommenden Packete an aller anderen verbundenen Clients"
        try:
            # handshake:
            if self.recv() != "Chat_certified_client":
                print(self.recv)

                self.sockt.clients[self.num].close()
                self.sockt.clients[self.num] = None

                print("SocketServer - " + str(self.sockt.addr[self.num]) + " not certified")
                print("SocketServer - " + "Slot " + str(self.num) + " is now available")
                self.sockt.slot[self.num] = 0
                return

            self.send("ok")

        except socket.error:
            self.closeClient()
            return

        print("SocketServer - " + "successful handshake")

        while True:
            try:
                textn = self.sockt.clients[self.num].recv(1024)
                if textn != b'':

                    for i in range(len(self.sockt.clients)):
                        if i != self.num and self.sockt.slot[i] == 1 and (
                                self.sockt.clients[i] != 0 and self.sockt.clients[i] != None):

                            self.sockt.clients[i].sendall(textn)
                        else:
                            pass
                else:
                    self.closeClient()
                    break

            except socket.error:
                self.closeClient()
                break


if __name__ == "__main__":
    s = socketServer(host_ip, port)  # öffnet den Server