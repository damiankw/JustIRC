import JustIRC
import requests
import re

bot = JustIRC.IRCConnection()

def on_connect(bot):
    bot.send_nick("TitleBot")
    bot.send_user("TitleBotTest")

def on_welcome(bot):
    bot.send_join("#JustIRCTest")

def on_text(bot, nick, chan, text):
    for message_part in text.split():
        if message_part.startswith("http://") or message_part.startswith("https://"):
            html = requests.get(message_part).text
            title_match = re.search("<title>(.*?)</title>", html)
            if title_match:
                bot.send_msg(chan, "Title of the URL by {}: {}".format(nick, title_match.group(1)))

bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_text.append(on_text)

bot.connect("irc.freenode.net")
bot.run_loop()
