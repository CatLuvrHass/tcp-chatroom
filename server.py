import threading
import socket

host = '127.0.0.0' # local host
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

# broadcast method
def broadcast(message):
    for client in clients:
        client.send(message)

    
# handling the client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# main recieve method
def receive():
    while True:
        # accept clients connection req and 
        # print confirmation when they do so Server Admin knows
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        # send to the client keyword "nick"
        # so the client knows to send their name
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
receive()