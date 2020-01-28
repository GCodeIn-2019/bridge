# bridge
Bridge to connect any number of chat platforms, with prebuilt modules for IRC
and Discord

## API
A bridge module is basically a bot for whichever chat platform it adds to the
bridge. When it receives a message, it should call `bridge.send(user,
message)`. It should also define it own function, `send(platform, user,
message)`. `bridge` will call this function when it receives a message from
any other platform.
