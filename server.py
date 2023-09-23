import threading
import socket
import common

class Server:
    """
        Server class will host and handle users.
    """

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__clients = []
        self.__nicknames = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.__host, self.__port))
        print('Server is listening...')
        self.server.listen()

    def broadcast(self, message):
        for client in self.__clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.__clients.index(client)
                self.__clients.remove(client)
                client.close()
                nickname = self.__nicknames[index]
                self.broadcast(f'{nickname} left the chat!'.encode(common.ENCODING))
                break

    def host(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')

            client.send(common.KEYWORD.encode(common.ENCODING))
            nickname = client.recv(1024).decode(common.ENCODING)
            self.__nicknames.append(nickname)
            self.__clients.append(client)

            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} joined the chat!'.encode(common.ENCODING))
            client.send('Connected to the server!'.encode(common.ENCODING))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

server = Server(common.HOST_NAME, common.PORT)
server.host()