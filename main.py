import discord
import openai
import os
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.all()
client = discord.Client(intents=intents)

monkey_words = ["monkey", "monke"]
monkey_facts = ["A howler monkey can be heard from 3 miles away", 
               "pygmy monkeys are the smallest of the monkey species"]

def get_monkey():
  return "https://www.placemonkeys.com/500"

def get_fact(prompt, model):

  response = openai.chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": prompt}]
  )

  return response.choices[0].message.content


def update_facts(monkey_fact):
  if "facts" in db.keys():
    facts = db["facts"]
    facts.append(monkey_fact)
    db["facts"] = facts
  else:
    db["facts"] = ["monkey_fact"]

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$monkey'):
    await message.channel.send("OOH")

  # options = monkey_facts
  # if "facts" in db.keys():
  #   options = options + db["facts"]

  if any(word in msg for word in monkey_words):
    fact = "give me a fact about monkeys"
    await message.channel.send(get_monkey())
    await message.channel.send(get_fact(fact, model="gpt-3.5-turbo"))

  if msg.startswith('$new'):
    monkey_fact = msg.split("$new ", 1)[1]
    update_facts(monkey_fact)
    await message.channel.send("New Fact Added!")

keep_alive()
my_secret = os.environ['TOKEN']
openai.api_key = os.environ['CHAT_GPT_KEY']
client.run(my_secret)
