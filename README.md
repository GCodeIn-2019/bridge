# bridge
General-purpose chat bridge

## Concept
Let's say you want to bridge IRC and Discord. Usually, you would write a
hybrid IRC-Discord bot that relayed messages. However, there is a
fundamental problem with this: suppose you want to add Slack. Now, you
probably wrote the bridge in a way that only supported two platforms. You have
to rewrite it. But later, you keep adding more platforms: Gitter, WhatsApp,
and several game chats. Your bridge quickly becomes huge, unwieldy, and
unmaintainable.

`bridge` (creative name, huh?) solves that. It is actually NOT a chat bridge.
It as a chat __server__. Wait, what? Yes, it's a chat server. Except that it
is not meant to run on a network, but a local machine. Back to the IRC-Discord
example, you don't directly bridge IRC and Discord. Instead, you bridge
IRC-`bridge` and Discord-`bridge`. This effectively bridges IRC-Discord. But,
why? Well, when you add Slack, you just bridge Slack-`bridge`. Gitter? Same
thing. Any bot-able platform can be connected to `bridge`. Technically, there
is no reason you can't connect SMS.

Modules are responsible for formatting the messages they receive into actual
human-readable ones. This is done so modules may show messages in whatever way
is conventional for that particular platform, to reduce confusion.

## API
`bridge` is extremely flexible. Any language that can connect to a UNIX domain
socket can be used to make a `bridge` bridge.
### Encoding
`bridge` only allows UTF-8. If you are using an ASCII-only platform, don't
worry; all valid ASCII text means exactly the same thing in UTF-8. If your
platform uses a different charset, be careful! You will most likely need to
do some charset conversion.
### Socket location
The socket is located at `/tmp/chatbridge`.
### Initialization
First, connect to `/tmp/chatbridge`. Next, send a Unicode string describing
your platform in a human-readable way, e.g. `IRC` or `Discord`, followed by
`0xFF`.
### Sending messages
Messages are sent to `bridge` in a JSON-based format. The body of the message
consists of a JSON object with properties `sender` and `message`, containing
the respective values (as strings). The entire message is `0xFE`, then the
body, then `0xFF`.

    <0xFE>{"sender":"hello", "message":"world"}<0xFF>

You are responsible for not telling `bridge` about your own messages. Be
careful with this, as you could quite easily end up with an infinite loop, not
to mention a very annoying channel flood!

### Receiving messages
`bridge` sends its messages in nearly the same format as it expects to receive
them. The only difference is an added property, `platform`, the human-readable
name of the platform on which the message originated.

    <0xFE>{"platform":"IRC", "sender":"hello", "message":"world"}<0xFF>

You are responsible for formatting the messages into actual text to send to
the chat. This is to allow you to use a format that looks the least
out-of-the-ordinary on your platform. The best format for showing messages on
IRC may not be the same as the best format for Discord.

## Included bridges
We include two bridges. One, `ircbridge.py`, is a "real" bridge for IRC. Just run it
with no arguments for usage information.

The other, `msggen.py`, simply sends out a message every second for testing
your bridges. It doesn't currently do anything when receiving messages. Don't
run it when you also have "real" chat rooms/channels connected! It is quite
annoying.
