from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Server_cl():
    def __init__(self):
        self.addresses = {}
        self.clients = {}
        self.HOST = '127.0.0.1'
        self.PORT = 34000

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)

        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(self.ADDR)

    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = self.SERVER.accept()
            print(str(client_address) + " has connected.")
            #client.send(bytes("Welcome ", "utf8"))
            #client.send(bytes("If you ever want to quit, type {quit} to exit", "utf8"))
            self.addresses[client] = client_address
            #print(self.addresses)
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self,client):  # Takes client socket as argument.
        """Handles a single client connection."""

        name = client.recv(self.BUFSIZ).decode("utf8")
        welcome = "Welcome " + name + " If you ever want to quit, type {quit} to exit."
        client.send(bytes(welcome, "utf8"))
        msg = name + " has joined the chat!"
        print(msg)
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name
        print(str(len(self.clients)) + " Clienten sind verbuden")

        while True:
            msg = client.recv(self.BUFSIZ)
            # Sende Nachricht an alle
            if msg != bytes("{quit}", "utf8"):
                self.broadcast(msg, name + ": ")
            # Falls quit eingeben wird, beende Verbindung
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del self.clients[client]
                self.broadcast(bytes(name + " has left the chat.", "utf8"))
                print(name + " has left the chat.")
                print(str(len(self.clients)) + " Clienten sind verbuden")
                break

    def broadcast(self,msg, prefix=""):  # prefix ist für name identification.
        """Broadcasts eine message zu allen clients."""
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

if __name__ == "__main__":
    sev = Server_cl()
    sev.SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=sev.accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    sev.SERVER.close()