import JustIRC
import requests

bot = JustIRC.IRCConnection()

def on_connect(bot):
    bot.send_nick("WeatherBot")
    bot.send_user("WeatherBot")

def on_welcome(bot):
    bot.send_join("#JustIRCTest")

def on_text(bot, nick, chan, text):
    if len(text.split()) == 0:
        text = "." #For people who try to crash bots with just spaces

    if text.split()[0] == "!weather":
        if len(text.split()) > 1:
            weather_data = requests.get("http://api.openweathermap.org/data/2.5/weather", params={"q": text.split(" ", 1), "units": "metric"}).json()
            if weather_data["cod"] == 200:
                bot.send_msg(chan, "The weather in {} is {} and {} degrees.".format(weather_data["name"], weather_data["weather"][0]["description"], weather_data["main"]["temp"]))
        else:
            bot.send_msg(chan, "Usage: !weather Istanbul")
    elif text.split()[0] == "!test":
        bot.send_msg(chan, "Test successful!")

bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_text.append(on_text)

bot.connect("irc.freenode.net")
bot.run_loop()
