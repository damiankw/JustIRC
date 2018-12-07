import JustIRC
import requests

whoischan = "#JustIRCTest"
relaychan = "#JustIRCTest"

bot = JustIRC.IRCConnection("WhoisBot", "WhoisBot", "I will WHOIS you!")

def on_welcome(bot):
    bot.send_join("{},{}".format(whoischan, relaychan))

def on_join(bot, nick, chan):
    if (chan.lower() == whoischan.lower()):
        bot.send_line("WHOIS {}".format(nick))
    
def on_whois(bot, cmd, prefix, args):
    if (cmd == "311"):
        bot.send_msg(relaychan, "*** WHOIS for {} ***".format(args[1]))
        bot.send_msg(relaychan, "Address    : {}!{}@{} ({})".format(args[1], args[2], args[3], args[5]))
    elif (cmd == "319"):
        bot.send_msg(relaychan, "Channels   : {}".format(args[2]))
    elif (cmd == "312"):
        bot.send_msg(relaychan, "Server     : {} ({})".format(args[2], args[3]))
    elif (cmd == "671"):
        bot.send_msg(relaychan, "Additional : {}".format(args[2]))
    elif (cmd == "330"):
        bot.send_msg(relaychan, "Additional : {}".format(" ".join(args[2:])))
    elif (cmd == "318"):
        bot.send_msg(relaychan, "*** End of WHOIS ***")


bot.on_welcome.append(on_welcome)
bot.on_join.append(on_join)
bot.on_unspecified.append(on_whois)

bot.connect("irc.freenode.net")
bot.run_loop()
