import bridge
def main():
    while True:
        bridge.send('user', 'hello')
