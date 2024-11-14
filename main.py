import discord
import wikipediaapi
import os
from dotenv import load_dotenv

from server import keep_alive
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

  def print_categorymembers(categorymembers, level=0, max_level=1):
    result = ""
    for c in categorymembers.values():
      result += "%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns)
      if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
        result += print_categorymembers(c.categorymembers,
                                        level=level + 1,
                                        max_level=max_level)
    return result

  async def send_long_message(channel, message):
    chunk_size = 2000
    for i in range(0, len(message), chunk_size):
      await channel.send(message[i:i + chunk_size])

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    msg = message.content
    if msg.startswith("$search"):
      search = msg.split("$search ", 1)[1]
      wiki = wikipediaapi.Wikipedia("https://github.com/salam002/wikiBot",
                                    'en')
      page = wiki.page(search)
      if page.exists():
        await message.channel.send(page.summary[0:1150])
      else:
        await message.channel.send("Page does not exist")

    if msg.startswith("$categories"):
      search = msg.split("$categories ", 1)[1]
      wiki = wikipediaapi.Wikipedia('https://github.com/salam002/', 'en')

      wiki_wiki = wiki.page(search)

      if wiki_wiki.exists():
        cat = wiki.page(f"Category: {search}")
        print(f"Category members: Category: {search}")
        category_members = print_categorymembers(cat.categorymembers)
        await send_long_message(
            message.channel,
            f"Category members of '{search}':\n{category_members}")
      else:
        await message.channel.send(f"Category '{search}' does not exist.")

  keep_alive()
  client.run(token)
else:
  print("Error: TOKEN not found")
