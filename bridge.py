#!/usr/bin/env python3
#bridge.py - "meta-chat" system for bridging platforms
import socket
import threading
import os
import json
server_address = '/tmp/chatbridge'
try:
    os.unlink(server_address)
except FileNotFoundError:
    pass
platforms = []
def transmit(l):
    for platform in platforms:
        if l['platform'] != platform.name:
            platform.send(json.dumps(l))
    print(l)

class Platform(threading.Thread):
    def __init__(self, csocket):
        threading.Thread.__init__(self)
        self.csocket = csocket
        self.receiving = False

    def send(self, message):
        self.csocket.sendall(bytes([0xFE]) + bytes(message, 'utf-8') + bytes([0xFF]))

    def run(self):
        print('connection!')
        name = b''
        while True:
            name += self.csocket.recv(1)
            if 0xFF in name:
                self.name = name[:-1].decode('utf-8')
                break
        buf = b''
        while True:
            byte = self.csocket.recv(1)
            if self.receiving:
                if byte == bytes([0xFF]):
                    message = json.loads(buf.decode('utf-8'))
                    message['platform'] = self.name
                    transmit(message)
                    self.receiving = False
                    buf = bytes()
                else:
                    buf += byte
            else:
                if byte == bytes([0xFE]):
                    self.receiving = True
                    buf = bytes()

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind(server_address)
while True:
    sock.listen(1)
    clientsock, _ = sock.accept()
    newthread = Platform(clientsock)
    newthread.start()
    platforms.append(newthread)
