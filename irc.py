import bridge
import sys
import argparse
import itertools
import socket
def send(platform, user, message, action):
    if action:
        message = "{}: * {} {}".format(platform, user, message)
    else:
        message = "{}: <{}> {}".format(platform, user, message)
    irc.sendall(bytes('PRIVMSG ##gci-2019 :{}\n'.format(message), 'utf-8'))

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect(('irc.freenode.net', 6667))
irc.sendall(bytes("USER {} 0 * :{}\r\n".format('GracieBridge', 'IRC-Discord Bridge'), 'utf-8'))
irc.sendall(bytes("NICK {}\r\n".format('GracieBridge'), 'utf-8'))
irc.sendall(bytes("JOIN {}\r\n".format('##gci-2019'), 'utf-8'))
def main():
    pass
