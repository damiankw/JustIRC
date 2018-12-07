# What is JustIRC
JustIRC is a single-file IRC library that allows you to write simple IRC bots
without having to deal with large frameworks. It's designed to be simple rather
than feature-rich. That doesn't mean it doesn't have the necessary feautures for
an IRC bot though.

JustIRC is

* Event-based.
* Handles pings automatically so you don't have to
* Written in pure Python. Uses sockets instead of heavy frameworks.
* Has simple functions for most IRC functionality. You don't have to touch a
  line of socket code.

# Examples
* [ParrotBot](examples/parrotbot.py) - A bot that replies to you with the same message, just like a parrot.  
* [HelloBot](examples/hellobot.py) - A bot that greets people who say "Hi" or "Hello".  
* [WeatherBot](examples/weatherbot.py) - A bot that responds to "!weather Istanbul" with the current weather. *Currently broken due to weather system requiring API token*
* [TitleBot](examples/titlebot.py) - A bot that responds with the titles of URLs posted to the channel.
* [WhoisBot](examples/whoisbot.py) - A bot which /whois's users on join to one channel and spits WHOIS information out in another.

# Documentation and Examples
The library is quite new so I haven't found the time to document it yet. I will
try adding some examples soon.
