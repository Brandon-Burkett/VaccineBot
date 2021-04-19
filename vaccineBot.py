import discord
from discord.ext import tasks, commands
import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')

client = discord.Client()


@tasks.loop(seconds=600.0)
async def vaccineCheck():
    channel = client.get_channel(833444408581554196)
    cities_list = ["LEWISBURG", "MILTON", "NORTHUMBERLAND",
                   "MIFFLINBURG", "WATSONTOWN", "SUNBURY", "SELINSGROVE", "DANVILLE"]

    response = requests.get(
        'https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.PA.json',
        headers={
            'Referer': 'https://www.cvs.com/immunizations/covid-19-vaccine'},
    )
    payload = response.json()

    for item in payload["responsePayloadData"]["data"]["PA"]:
        if item['city'] in cities_list:
            if item['status'] != 'Fully Booked':
                await channel.send('@everyone')
                await channel.send(item['city'] + ": " + item['status'])
            # await channel.send(item['city'] + ": " + item['status'])
            print(item['city'] + ": " + item['status'])

@client.event
async def on_ready():
    print(f"""I am logged in as {client.user}""")
    vaccineCheck.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!hello"):
        await message.channel.send("Hello how are you!")

client.run(os.getenv('DISCORD_BOT_TOKEN'))
