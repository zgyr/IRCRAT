import socket
import time

class IRC:
    
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'irc.esper.net'
        self.port = 6667
        self.name = 'randomname987654'
    
    def send_raw(self, message):
        self.socket.send(bytes(message + '\r\n', 'UTF-8'))
    
    def send(self, target, message):
        self.send_raw(f'PRIVMSG {target} {message}')
    
    def connect(self):
        self.socket.connect((self.server, self.port))
        time.sleep(1)
        self.send_raw(f'USER {self.name} . . :{self.name}')
        self.send_raw(f'NICK {self.name}')
    
    def response(self):
        time.sleep(1)
        resp = self.socket.recv(2048).decode('UTF-8')
        if resp.find('PING') != -1:
            self.send_raw('PONG ' + resp.split()[1])