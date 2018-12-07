# JustIRC Documentation

## 1. What is JustIRC
JustIRC is an event-driven IRC library written in pure Python. It doesn't depend
on any non-standard libraries.

## 2. Hello World
Here's a simple example, before explaining the API functions. This bot will
reply to anyone who says "Hello".

```python
import JustIRC

bot = JustIRC.IRCConnection("HelloWorldBot", "HelloBot", "I love greetings!")
bot.debug = True
def on_welcome(bot):
    bot.send_join("#HelloTest")

def on_text(bot, nick, chan, text):
    if "hello" in text.lower():
        bot.send_msg(chan, "Hello there {}!".format(nick))

bot.on_welcome.append(on_welcome)
bot.on_text.append(on_text)

bot.connect("irc.freenode.net")
bot.run_loop()
```

## 3. More examples
You can find more example code in [the examples directory](../../tree/master/examples).

## 4. The IRCConnection Class
IRCConnection is the main class of this library. It handles the connection,
parses and creates the packets and handles the events.

### 4.1 Option Variables
There are a number of variables which can be written to directly in order to manipulate how
the IRCConnection instance will act. Most of these are set when creating the bot and may differ from actual detail.

| Variable      | Valid data  | Default | Description |
| --------      | ----------  | ------- | ----------- |
| debug         | True\|False | False   | When set to True will output all data sent to/receieved from the server connection to the console. |
| autoreconnect | True\|False | True    | When set to True will automatically try and reconnect to the server if disconnected. When set to false will quit the application. |
| timeout       | Integer     | 60      | Number of seconds to wait in between connection attempts. |
| nick          | String      | ""      | The nickname of the bot, for use when connecting. |
| user          | String      | ""      | The username of the bot, for use when connecting. |
| name          | String      | ""      | The real name of the bot, for use when connecting. |
| server        | String      | ""      | The server/ip the bot is connecting to. |
| port          | String      | ""      | The port the bot is connecting to. |
| password      | String      | ""      | The password to the connecting server. |


### 4.2 Output Variables
These variables are used to store data about the connection, the bot, and other things a standard irc client/bot should hold. These are the actual details.

| Variable  | Data Type    | Description |
| --------  | ---------    | ----------- |
| botnick   | String       | The nickname of the bot. |
| botuser   | String       | The username of the bot. |
| bothost   | String       | The hostname of the bot. |
| botname   | String       | The real name of the bot. |
| botserver | String       | The server the bot is connected to. |
| botmode   | String       | The current usermode of the bot. *(in development)* |
| botchan   | String-Array | The channels the bot is currently on. |

### 4.3 Functions
The functions are what do your core bot is made out of, these allow you to get the bot to do things. Arguments with a question mark in front of them are optional and have a default value of some kind.

| Function    | Arguments                     | Description |
| --------    | ---------                     | ----------- |
| connect     | (server/ip, ?port, ?password) | Connects the bot to a new server, with an optional port and server password. |
| send_line   | (data)                        | Sends data directly to the server. |
| send_msg    | (target, message)             | Sends a message to a nick/chan. |
| send_notice | (target, message)             | Sends a notice to a nick/chan. |
| send_action | (target, message)             | Sends an action (/me) to a nick/chan. |
| send_join   | (channel)                     | Joins a channel. |
| send_part   | (channel, ?message)           | Part a channel with an optional message. |
| send_nick   | (nickname)                    | Changes the bot nickname. *Can be used on_connect* |
| send_user   | (username, ?realname)         | Sends a username and optional real name. *Can only be used on_connect* |
| send_quit   | (?message)                    | Quits the network with an optional message. |
| send_kick   | (chan, nick, ?message)        | Kicks a user from a channel with an optional message. |

### 4.4 Events
There are multiple events that can be used for different purposes. Append your own functions to different events to create your bot.

| Event              | Arguments | Description |
| -----              | --------- | ----------- |
| on_packet_received | (data) | When any packet is received (raw data) |
| on_connect         | () | When the socket connects to the server |
| on_disconnect      | () | When the socket disconnects from the server |
| on_action          | (nick, target, message) | When someone /me's |
| on_text            | (nick, chan, message) | When someone messages a channel |
| on_query           | (nick, message) | When someone messages the bot |
| on_ping            | () | When the server sends ping |
| on_welcome         | () | When the server shows the client as connected |
| on_join            | (nick, chan) | When someone joins a channel |
| on_part            | (nick, chan, message) | When someone parts a channel |
| on_mode            | (nick, chan, mode, args) | When a channel mode is changed |
| on_usermode        | (mode, args) | When the bot mode changes |
| on_kick            | (nick, chan, knick, message) | When someone is kicked from a channel |
| on_nick            | (nick, newnick) | When someone changes their nickname |
| on_notice          | (nick, target, message) | When someone notices the bot (or channel) |
| on_quit            | (nick, message) | When someone quits the network |
| on_topic           | (nick, chan, topic) | When a channel topic is changed |
| on_ctcp            | (command, target, nick, message) | When a ctcp is received |
| on_ctcpreply       | (command, nick, message) | When a ctcp reply is received |
| on_whoreply        | (channel, username, hostname, server, nick, away status, hops, realname) | When /who responds |
| on_unspecified     | (command, server/user, [array]arguments) | When any other command is sent through unknown to JustiRC |
