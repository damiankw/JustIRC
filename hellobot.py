import JustIRC
import random

bot = JustIRC.IRCConnection()

greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!"
]

def on_connect(bot):
    bot.send_nick("HelloBot")
    bot.send_user("HelloBot")

def on_welcome(bot, server):
    bot.send_join("#HelloBotTest")

def on_text(bot, nick, chan, text):
    if "hi" in text.lower() or "hello" in text.lower():
        greeting_message = random.choice(greetings).format(nick)
        bot.send_msg(chan, greeting_message)

bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_text.append(on_text)

bot.connect("irc.freenode.net")
bot.run_loop()
