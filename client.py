import socket 
import threading
import common 

class Client:
    """ 
        client class will model the user
        @__nickname: a name chosen by the user and sent to server 
        after ack message is recieved.
    """

    def __init__(self, nickname):
        self.__nickname = nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.client.connect((host,port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode(common.ENCODING)
                if message == common.KEYWORD:
                    self.client.send(self.__nickname.encode(common.ENCODING))
                else:
                    print(f'{message} ')
            except:
                print('an error occured')
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.__nickname}: {input("")}'
            self.client.send(message.encode(common.ENCODING))

    def join_chat(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()    

nickname = input('Choose a nickname: ')
user = Client(nickname)
user.connect(common.HOST_NAME, common.PORT)
user.join_chat()