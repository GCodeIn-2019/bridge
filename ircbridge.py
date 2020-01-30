#! /usr/bin/env python
# bridge <-> IRC bridge
#
# from https://github.com/jaraco/irc/blob/master/scripts/testbot.py
#
# Example program using irc.bot.
#
# Joel Rosdahl <joel@rosdahl.net>

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import json
import socket
import threading

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect('/tmp/chatbridge')
s.sendall(b'IRC' + bytes([0xFF]))
class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        print("warning, nick taken")
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        s.sendall(bytes([0xFE]) + bytes(json.dumps({"message": e.arguments[0], "sender": e.source.split('!')[0]}), 'utf-8') + bytes([0xFF]))

def listen():
    buf = b''
    receiving = False
    while True:
        byte = s.recv(1)
        if receiving:
            if byte == bytes([0xFF]):
                data = json.loads(buf.decode('utf-8'))
                message = '[{}] <{}> {}'.format(data['platform'], data['sender'], data['message'])
                bot.connection.privmsg(channel, message)
                receiving = False
                buf = bytes()
            else:
                buf += byte
        else:
            if byte == bytes([0xFE]):
                receiving = True
                buf = bytes()

def main():
    import sys
    global bot
    global channel
    if len(sys.argv) != 4:
        print("Usage: testbot <server[:port]> <channel> <nickname>")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]
    thread = threading.Thread(target=listen)
    thread.start()
    bot = Bot(channel, nickname, server, port)
    bot.start()


if __name__ == "__main__":
    main()
