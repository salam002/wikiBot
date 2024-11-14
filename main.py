import discord
import wikipediaapi
import os
from dotenv import load_dotenv

from replit import db

load_dotenv()
token = os.getenv('TOKEN')

if token:

  # user will enter topic and wikipedia will return the summary of    # the topic
  intents = discord.Intents.default()
  intents.message_content = True

  client = discord.Client(intents=intents)
  @client.event
  async def on_ready():
    print('We have logged in as {0.user}'.format(client))

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    msg = message.content
    if msg.startswith("$search"):
      search = msg.split("$search ", 1)[1]
      wiki = wikipediaapi.Wikipedia("https://github.com/salam002/wikiBot",'en')
      page = wiki.page(search)
      if page.exists():
        await message.channel.send(page.summary[0:2000])
      else:
        await message.channel.send("Page does not exist")
  client.run(token)
else:
  print("Error: TOKEN not found")
    