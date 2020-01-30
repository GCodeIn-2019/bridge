#! /usr/bin/env python
# bridge <-> discord bridge
import json
import socket
import threading

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect('/tmp/chatbridge')
s.sendall(b'IRC' + bytes([0xFF]))
def send(sender, message):
    s.sendall(bytes([0xFE]) + bytes(json.dumps({"message": message, "sender": sender}), 'utf-8') + bytes([0xFF]))

def discordsend(text):
    #Put code here to send text to Discord

#when you get a message from discord, call send(sendername, messagetext)

def listen():
    buf = b''
    receiving = False
    while True:
        byte = s.recv(1)
        if receiving:
            if byte == bytes([0xFF]):
                data = json.loads(buf.decode('utf-8'))
                message = '[{}] <{}> {}'.format(data['platform'], data['sender'], data['message'])
                dicordsend(message)
                receiving = False
                buf = bytes()
            else:
                buf += byte
        else:
            if byte == bytes([0xFE]):
                receiving = True
                buf = bytes()

thread = threading.Thread(target=listen)
thread.start()
