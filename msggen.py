#! /usr/bin/env python
# bridge <-> IRC bridge
#
# from https://github.com/jaraco/irc/blob/master/scripts/testbot.py
#
# Example program using irc.bot.
#
# Joel Rosdahl <joel@rosdahl.net>

import socket
import json
import time

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect('/tmp/chatbridge')
s.sendall(b'Message Generator' + bytes([0xFF]))
while True:
    s.sendall(bytes([0xFE]) + bytes(json.dumps({"message": "If you are reading this on a chat platform, your bridge works!", "sender": "It_Works"}), 'utf-8') + bytes([0xFF]))
    time.sleep(1)
