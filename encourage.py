# This example requires the 'message_content' intent.
#########################################
import discord
import requests
import json
import random
# from replit import db
db = {}
# dictionary

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]
starter_encrg = [
    "Cheer Up!",
    "Hang in there.",
    "You are a great person."
]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "\n - " + json_data[0]['a']
    return quote


def upd_encrg(encrg_msg):
    if ("encouragements" in db.keys()):
        encrgs = db["encouragements"]
        encrgs.append(encrg_msg)
        db["encouragements"] = encrgs
    else:
        db["encouragements"] = [encrg_msg]


def del_encrg(index):
    encrgs = db["encouragements"]
    if (len(encrgs) > index):
        del encrgs[index]
        db["encouragements"] = encrgs


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    msg = message.content

    async def read_encrgs(x):
        k = list(x)
        for i in k:
            await message.channel.send(i)

    if (message.author == client.user):
        return

    if (msg.startswith("$hello")):
        await message.channel.send("Hello!!")

    if (msg.startswith("$inspire")):
        quote = get_quote()
        await message.channel.send(quote)

    options = starter_encrg
    if ("encouragements" in db.keys()):
        options = options + list(db["encouragements"])

    if (any(word in msg for word in sad_words)):
        await message.channel.send(random.choice(options))

    if (msg.startswith("$new")):
        encrg_msg = msg.split("$new ", 1)[1]
        upd_encrg(encrg_msg)
        await message.channel.send("New encouraging message added!")

    if (msg.startswith("$del")):
        encrgs = []
        if ("encouragements" in db.keys()):
            index = int(msg.split("$del ", 1)[1])
            del_encrg(index)
            encrgs = db["encouragements"]
        await read_encrgs(encrgs)

    if (msg.startswith("$clr")):
        if ("encouragements" in db.keys()):
            del db["encouragements"]
            await message.channel.send("The manualy added encouragements have been cleared!")
        else:
            await message.channel.send("There are no manual encouragements present.")

    if (msg.startswith("$list")):
        if ("encouragements" in db.keys()):
            await read_encrgs(db["encouragements"])
        else:
            await message.channel.send("There are no manual encouragements present.")


client.run(
    'MTA0ODc5NjE1ODMwODM5NzA5Ng.Gergu9.Csb-psYzSnGPFqfZneXaGqN-0S-4KfevWPCdNU')
