import threading
import socket
import time
import sys

class IRC:
    
    def __init__(self):
        self.server = 'irc.esper.net'
        self.port = 6667
        self.name = 'random_name000000'
        self.buffer = ''
    
    def get_raw(self):
        if self.buffer != '':
            line, self.buffer = self.buffer.split('\r\n', 1)
            prefix, command, args = '', '', ''
            if line[0] == ':':
                prefix, line = line[1:].split(' ', 1)
            if line.find(' :') != -1:
                args, line = line.split(' :', 1)
                args = args.split()
            return prefix, args, line
        else:
            return None
    
    def send_raw(self, message):
        self.socket.send(bytes(message + '\r\n', 'UTF-8'))
    
    def send(self, target, message):
        self.send_raw(f'PRIVMSG {target} {message}')
    
    def connect(self):
        self.online = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server, self.port))
        time.sleep(0.5)
        self.recvThread = threading.Thread(target = self.response)
        self.recvThread.start()
        self.send_raw(f'USER {self.name} . . :{self.name}')
        self.send_raw(f'NICK {self.name}')
    
    def disconnect(self):
        self.send_raw('QUIT')
        self.online = False
        time.sleep(0.5)
        self.socket.close()
        self.recvThread.join()
    
    def response(self):
        while self.online:
            try:
                time.sleep(0.2)
                resp = self.socket.recv(512).decode('UTF-8')
                if resp.find('PING') != -1:
                    self.send_raw('PONG ' + resp.split()[1])
                self.buffer += resp
            except OSError:
                time.sleep(3)
                self.connect()
            else:
                pass