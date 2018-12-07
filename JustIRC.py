import socket
import time
import ssl

def parse_irc_packet(packet):
    irc_packet = IRCPacket()
    irc_packet.parse(packet)
    return irc_packet

class IRCPacket:
    def __init__(self):
        self.prefix = ""
        self.command = ""
        self.line = ""
        self.arguments = []

    def parse(self, packet):
        self.line = packet
        if packet.startswith(":"):
            self.prefix = packet[1:].split(" ")[0]
            packet = packet.split(" ", 1)[1]

        if " " in packet:
            if " :" in packet:
                last_argument = " :".join(packet.split(" :")[1:])
                packet = packet.split(" :")[0]
                for splitted in packet.split(" "):
                    if not self.command:
                        self.command = splitted
                    else:
                        self.arguments.append(splitted)
                self.arguments.append(last_argument)
            else:
                for splitted in packet.split(" "):
                    if not self.command:
                        self.command = splitted
                    else:
                        self.arguments.append(splitted)
        else:
            self.command = packet

class IRCConnection:
    def __init__(self, nick="", user="", name=""):
        # set default values
        self.debug = False
        self.autoreconnect = True
        self.timeout = 60
        
        # pull in nick/user/name from the function
        self.nick = nick
        self.user = user
        self.name = name
        
        # set the user/name if they aren't set but nick is, otherwise we might not actually connect (if scripter is lazy)
        if nick != "" and user == "":
            self.user = nick
        if nick != "" and name == "":
            self.name = nick

        # set up default events
        self.on_packet_received = [];   # when a packet is received
        self.on_connect = [];           # when the socket connects to the server
        self.on_disconnect = [];        # when the socket disconnects from the server
        self.on_action = [];            # when someone /me's
        self.on_text = [];              # when someone messages a channel
        self.on_query = [];             # when someone messages the bot
        self.on_ping = [];              # when the server sends ping
        self.on_welcome = [];           # when the server shows the client as connected
        self.on_join = [];              # when someone joins a channel
        self.on_part = [];              # when someone parts a channel
        self.on_mode = [];              # when a channel mode is changed
        self.on_usermode = [];          # when the bot mode changes
        self.on_kick = [];              # when someone is kicked from a channel
        self.on_nick = [];              # when someone changes their nickname
        self.on_notice = [];            # when someone notices the bot (or channel)
        self.on_quit = [];              # when someone quits the network
        self.on_topic = [];             # when a channel topic is changed
        self.on_ctcp = [];              # when a ctcp is received
        self.on_ctcpreply = [];         # when a ctcp reply is received
        self.on_whoreply = [];          # when /who responds
        self.on_unspecified = [];       # when any other command is sent through unknown to JustiRC

    def run_once(self):
        packet = parse_irc_packet(next(self.lines)) #Get next line from generator

        for event_handler in list(self.on_packet_received):
            event_handler(self, packet)
            # on_packet_received(packet)

        if packet.command == "PRIVMSG" and packet.arguments[1].startswith("\x01ACTION"): # /me does something
            for event_handler in list(self.on_action):
                event_handler(self, packet.prefix.split("!")[0], packet.arguments[0], packet.arguments[1].split("\x01")[1][7:])
                # on_action(nick, target, text)
                
        elif packet.command == "PRIVMSG" and packet.arguments[1].startswith("\x01"): # /ctcp <bot/chan> something something
            for event_handler in list(self.on_ctcp):
                event_handler(self, packet.arguments[1].split()[0], packet.prefix.split("!")[0], packet.arguments[0], packet.arguments[1].split("\x01")[1][len(packet.arguments[1].split()[0]):])
                # on_ctcp(cmd, target, nick, text)
                
        elif packet.command == "PRIVMSG":
            if packet.arguments[0].startswith("#"):
                for event_handler in list(self.on_text):
                    event_handler(self, packet.prefix.split("!")[0], packet.arguments[0], packet.arguments[1])
                    # on_text(nick, chan, text)
            else:
                for event_handler in list(self.on_query):
                    event_handler(self, packet.prefix.split("!")[0], packet.arguments[1])
                    # on_query(nick, text)
                    
        elif packet.command == "PING":
            self.send_line("PONG :{}".format(packet.arguments[0]))

            for event_handler in list(self.on_ping):
                event_handler(self)
                # on_pong()
                
        elif packet.command == "433" or packet.command == "437":
            self.send_nick("{}_".format(self.nick))
            
        elif packet.command == "001":
            self.botserver = packet.prefix
            self.botnick = packet.arguments[0]
            self.send_line("WHO {}".format(self.botnick))
            
            for event_handler in list(self.on_welcome):
                event_handler(self)
                # on_welcome(server)
                
        elif packet.command == "352":
            if packet.arguments[0] == self.botnick:
                self.botuser = packet.arguments[2]
                self.bothost = packet.arguments[3]
            
            for event_handler in list(self.on_whoreply):
                event_handler(self, packet.arguments[1], packet.arguments[2], packet.arguments[3], packet.arguments[4], packet.arguments[5], packet.arguments[6], packet.arguments[7].split()[0], packet.arguments[7][len(packet.arguments[7].split()[0])+1:])
#               on_whoreply(self, chan, user, host, server, nick, away, hop, name)
            
                
        elif packet.command == "396":
            self.bothost = packet.arguments[1]
        elif packet.command == "JOIN":
            self.botchan.append(packet.arguments[0])
            
            for event_handler in list(self.on_join):
                event_handler(self, packet.prefix.split("!")[0], packet.arguments[0])
                # on_join(nick, chan)
        elif packet.command == "PART":
            for event_handler in list(self.on_part):
                event_handler(self, packet.prefix.split("!")[0], packet.arguments[0], packet.arguments[1])
                # on_part(nick, chan, text)
        elif packet.command == "MODE":
            print(packet.prefix, packet.arguments)
            if packet.arguments[0].startswith("#"):
                for event_handler in list(self.on_mode):
                    event_handler(self, packet.arguments[0], packet.prefix.split("!")[0], packet.arguments[1])
            else:
                for event_handler in list(self.on_usermode):
                    event_handler(self, packet.prefix.split("!")[0], packet.arguments[1])
        elif packet.command == "KICK":
            for event_handler in list(self.on_kick):
                event_handler(self, packet.prefix.split("!")[0], packet.arguments[0], packet.arguments[1], packet.arguments[2])
                # on_kick(nick, chan, knick, text)
        elif packet.command == "NICK":
            if packet.prefix.split("!")[0] == self.botnick:
                self.botnick = packet.arguments[0]

            for event_handler in list(self.on_nick):
                event_handler(self, packet.prefix.split("!")[0], packet.arguments[0])
                # on_nick(bot, nick, newnick)
        elif packet.command == "NOTICE":
            print(packet.prefix, packet.arguments)
            for event_handler in list(self.on_notice):
                event_handler(self, packet.arguments[0], packet.prefix.split("!")[0])
        elif packet.command == "QUIT":
            for event_handler in list(self.on_quit):
                event_handler(self, packet.prefix.split("!")[0], packet.arguments[0])
                # on_quit(nick, text)
        elif packet.command == "TOPIC":
            for event_handler in list(self.on_topic):
                event_handler(self, packet.prefix.split("!")[0], packet.arguments[0], packet.arguments[1])
                # on_topic(nick, chan, topic)

        else:
            for event_handler in list(self.on_unspecified):
                event_handler(self, packet.command, packet.prefix, packet.arguments)

    def run_loop(self):
        while self.status == True:
            self.run_once()

    def read_lines(self):
        buff = ""
        while True:
            buff += self.socket.recv(1024).decode("utf-8", "replace")
            # check for reconnection
            if not buff:
                self.status = False
                for event_handler in list(self.on_disconnect):
                    event_handler(self)
                if self.autoreconnect == True:
                    # reset the socket and reconnect
                    time.sleep(self.timeout)
                    self.reconnect()
                    
                else:
                    # send through a fake buffer to close the script
                    buff = "\r\n"
            while "\n" in buff:
                line, buff = buff.split("\n", 1)
                line = line.replace("\r", "")
                if self.debug == True:
                    print("<- {}".format(line))
                yield line

    def send_line(self, line):
        if self.debug == True:
            print("-> {}".format(line));
        self.socket.send("{}\r\n".format(line).encode("utf-8"))




    def connect(self, server, port=6667, password=""):
        # store the data for reconnect
        self.server = server
        self.port = port
        self.password = password
        
        # actually connect to the server
        self.reconnect()
        
        
    def reconnect(self):
        # internal use only variables
        self.status = False
        self.botserver = "";    # determined by 001 arg1
        self.botnick = "";      # determined by 001 arg3
        self.botuser = "";      # determined by WHO
        self.bothost = "";      # determined by WHO
        self.botmode = "";      # determined by MODE
        self.botchan = [];      # determined by JOIN

        # connect the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server, self.port))
        self.status = True
        self.lines = self.read_lines()
        
        # on_connect user event
        for event_handler in list(self.on_connect):
            event_handler(self)
            
        # put this after initial on_connect() for backwards compatibility
        if self.password != "":
            self.send_line("PASS {}".format(password))
        if self.nick != "":
            self.send_line("NICK {}".format(self.nick))
        if self.user != "":
            self.send_line("USER {} 0 * :{}".format(self.user, self.name))







    def send_msg(self, to, message):
        self.send_line("PRIVMSG {} :{}".format(to, message))

    def send_notice(self, to, message):
        self.send_line("NOTICE {} :{}".format(to, message))

    def send_action(self, to, action):
        self.send_message(to, "\x01ACTION {}\x01".format(action))

    def send_join(self, chan):
        self.send_line("JOIN {}".format(chan))

    def send_part(self, chan):
        self.send_line("PART {}".format(chan))
        
    def send_nick(self, nick):
        self.nick = nick
        self.send_line("NICK {}".format(nick))

    def send_user(self, username, realname=""):
        if realname == "":
            realname = username
        self.send_line("USER {} 0 * :{}".format(username, realname))

    def send_quit(self, text):
        self.send_line("QUIT :{}".format(text))
        
    def send_kick(self, chan, nick, text):
        self.send_line("KICK {} {} :{}".format(chan, nick, text))