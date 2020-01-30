#! /usr/bin/env python
# bridge logger

import json
import socket
import threading
import sys
import datetime

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect('/tmp/chatbridge')
s.sendall(b'Logger' + bytes([0xFF]))
buf = b''
receiving = False
date = datetime.date.today().strftime('%m-%d-%Y')
lastdate = date
f = open('{}/{}.txt'.format(sys.argv[1], date), 'a+')
while True:
    byte = s.recv(1)
    if receiving:
        if byte == bytes([0xFF]):
            data = json.loads(buf.decode('utf-8'))
            date = datetime.date.today().strftime('%m-%d-%Y')
            if date != lastdate:
                f = open('{}/{}.txt'.format(sys.argv[1], date), 'a+')
                lastdate = date
            message = '{} [{}] <{}> {}\n'.format(datetime.datetime.now().strftime('%H:%M'), data['platform'], data['sender'], data['message'])
            f.write(message)
            f.flush()
            receiving = False
            buf = bytes()
        else:
            buf += byte
    else:
        if byte == bytes([0xFE]):
            receiving = True
            buf = bytes()
