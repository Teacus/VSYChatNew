#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import os
import json


class Chatter_cl():
    def __init__(self):
        self.name = input('Enter name: ')
        ZIEL = input("Default Server? y or n: ")
        if ZIEL == "n":
            HOST = input('Enter host: ')
            PORT = input('Enter port: ')
            self.PORT = int(PORT)
            self.HOST = HOST
        else:
            self.PORT = 34000
            self.HOST = "127.0.0.1"

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)
    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = client_socket.recv(self.BUFSIZ).decode("utf8")
                msg_list.insert(tkinter.END, msg)
            except OSError:  # Possibly client has left the chat.
                break

    def send(self,event=None):  # event is passed by binders.
        """Handles sending of messages."""
        msg = my_msg.get()
        my_msg.set("")  # Clears input field.
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()
            top.quit()

    def on_closing(self,event=None):
        """This function is to be called when the window is closed."""
        my_msg.set("{quit}")
        self.send()
    def window(self):
        # Grafische Oberfläche erstellen
        top = tkinter.Tk()
        top.title("Chatter von " + self.name)

        messages_frame = tkinter.Frame(top)
        my_msg = tkinter.StringVar()  # For the messages to be sent.
        # my_msg.set("Type your messages here.")
        scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
        # Following will contain the messages.
        msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        msg_list.pack()
        messages_frame.pack()

        # Erstellt Eingabefeld
        entry_field = tkinter.Entry(top, textvariable=my_msg)
        entry_field.bind("<Return>", chat.send)
        entry_field.pack()
        # Erstellt Send Button
        send_button = tkinter.Button(top, text="Send", command=chat.send)
        send_button.pack()
        # Erstellt Quit Button
        quit_button = tkinter.Button(top, text="Quit", command=chat.on_closing)
        quit_button.pack(side="right")

        top.protocol("WM_DELETE_WINDOW", chat.on_closing)

chat = Chatter_cl()

# Grafische Oberfläche erstellen
top = tkinter.Tk()
top.title("Chatter von " + chat.name)

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
#my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

# Erstellt Eingabefeld
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", chat.send)
entry_field.pack()
# Erstellt Send Button
send_button = tkinter.Button(top, text="Send", command=chat.send)
send_button.pack()
# Erstellt Quit Button
quit_button = tkinter.Button(top, text="Quit", command=chat.on_closing)
quit_button.pack(side="right")

top.protocol("WM_DELETE_WINDOW", chat.on_closing)

#----Now comes the sockets part----


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(chat.ADDR)
my_msg.set(chat.name)
chat.send(chat.name)
receive_thread = Thread(target=chat.receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
