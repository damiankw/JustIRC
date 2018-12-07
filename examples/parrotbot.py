import JustIRC

bot = JustIRC.IRCConnection()

def on_connect(bot):
    bot.send_nick("ParrotBotGk")
    bot.send_user("ParrotBotGk")

def on_welcome(bot):
    bot.send_join("#JustIRCTest")

def on_text(bot, nick, chan, text):
    bot.send_msg(chan, text)


bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_text.append(on_text)

bot.connect("irc.freenode.net")
bot.run_loop()
