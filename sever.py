# author: Amaury Lekens

import socket
import sys
import threading
from json import *

global connnected
SERVERADDRESS = (socket.gethostname(), 6000)

class AdderServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        print('ecoute sur {}:{}'.format(socket.gethostname(), 6000))


    def run(self):
        self.__s.listen(10)
        while True:
            try:
                with open("connected.txt","r") as file :
                    document=file.read()
                    connnected=loads(document)
                    client, addr = self.__s.accept()
                    newClient = {'username': self._clientUsername(client), 'client':client, 'adrr':addr}
                    connnected[self._clientUsername()]=newClient
                    print(connnected)

            except OSError:
                pass

    def _clientUsername(self,client):
        try:
            data= client.recv(1024).decode()
            return data
        except socket.timeout:
            pass
        except OSError:
            return

class AdderClient():
    def __init__(self):
        self.__s = socket.socket()
        print(self.__s.getsockname())
        self.__s.settimeout(0.5)

    def _connect(self, username):
        self.__s.connect(SERVERADDRESS)
        totalsent = 0
        msg = username
        try:
            while totalsent < len(msg):
                sent = self.__s.send(msg[totalsent:])
                totalsent += sent
        except OSError:
            print("Erreur lors de l'envoi du message.")


    def run(self):
        handlers = {
            '/connect': self._connect,
        }
        while True:
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ')+1:].rstrip()
            # Call the command handler
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                    pass
            else:
                print('Command inconnue:', command)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        Server =AdderServer()
        Server.run()
    elif len(sys.argv) == 3 and sys.argv[1] == 'client':
        AdderClient.run()
