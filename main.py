from replit import db
import os
import discord
import requests
import json
import random
import praw
from Keep_running import keep_running

client = discord.Client()
my_token = os.environ['TOKEN']
reddit_secret = os.environ['reddit_key']
reddit = praw.Reddit(client_id='HtqTteWA0F12ntEkYYJ0fQ',
                     client_secret=reddit_secret,
                     username='Gullible_Location',
                     password='wGrDp!7b!8GL#/J',
                     user_agent='auxiliator')

sad_words = ["sad", "depressed", "misserable", "down", "kms", "fuck"]

basic_cheers = ["cheer up", "King", "heads up king", "dont cry girl"]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = '"' + json_data[0]['q'] + '"' + " - " + json_data[0]['a']
    return (quote)


def update_cheers(message):
    if "cheers" in db.keys():
        cheers = db["cheers"]
        cheers.append(message)
        db["cheers"] = cheers
    else:
        db["cheers"] = [message]


def delete_cheers(index):
    cheers = db["cheers"]
    if len(cheers) > index:
        del cheers[index]
        db["cheers"] = cheers


def get_nasa_img():
    my_secret = os.environ['nasa_img']
    response = requests.get("https://api.nasa.gov/planetary/apod?api_key=" +
                            my_secret)
    json_data = json.loads(response.text)
    apod_url = json_data.get('url')
    return (apod_url)


def get_weather(city):

    my_secret = os.environ['weather_key']
    weather_key = my_secret
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=" + city +
        "&appid=" + weather_key)
    json_data = json.loads(response.text)
    weather = "The weather in " + city + " is " + (
        json_data.get('weather')
    )[0]['description'] + " with average temperature being " + format(
        ((json_data.get('main')).get('temp') - 272), '.2f')
    return (weather)


def get_ye_quote():
    response = requests.get("https://api.kanye.rest")
    json_data = json.loads(response.text)
    quote = json_data.get('quote')
    return (quote)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    print(db.keys())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!hello'):
        await message.channel.send(f"Hello! {message.author.mention}")

    if message.content.lower().startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        option = basic_cheers
        if "cheers" in db.keys():
            option = option + db["cheers"].value

        if any(word in message.content for word in sad_words):
            await message.channel.send(random.choice(option))

    if message.content.lower().startswith('!new'):
        upbeat_message = message.content.split("!new ", 1)[1]
        update_cheers(upbeat_message)
        await message.channel.send("Message Added")

    if message.content.lower().startswith('!del'):
        cheers = []
        if "cheers" in db.keys():
            index = int(message.content.split('!del ', 1)[1])
            delete_cheers(index)
            cheers = db["cheers"]
        await message.channel.send(cheers.value)

    if message.content.lower().startswith('!list'):
        cheers = []
        if "cheers" in db.keys():
            cheers = db["cheers"]
        await message.channe.send(cheers)

    if message.content.lower().startswith("!responding"):
        value = message.content.split("!responding ", 1)[1]

        if value.lower():
            db["responding"] = True
        else:
            db["respoding"] = False

        await message.channel.send("Responses are on now")

    if message.content.lower().startswith('!nasaapod'):
        img = get_nasa_img()
        await message.channel.send(img)

    if message.content.lower().startswith('!weather'):
        city = message.content.split('!weather ', 1)[1]
        weather = get_weather(city)
        await message.channel.send(weather)

    if message.content.lower().startswith('!ye'):
        ye_quote = get_ye_quote()
        await message.channel.send(ye_quote)

    if message.content.lower().startswith('!reddit'):
      sub = message.content.split('!reddit ',1)[1]
      subreddit = reddit.subreddit(sub)

      all_subs=[]
      top_subs=subreddit.hot(limit=100)

      for item in top_subs:
        all_subs.append(item)

      random_sub = random.choice(all_subs)

      name_post = random_sub.title
      url_post = random_sub.url

      embeded_message = discord.Embed(title=name_post)

      embeded_message.set_image(url = url_post)

      await message.channel.send(embed = embeded_message)



keep_running()
client.run(my_token)













