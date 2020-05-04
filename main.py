import os, discord
from discord.ext import commands
from dotenv import load_dotenv
from codeforces import test
from random import choice

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Done")

@bot.command(name='insult', help='Roasts someone', aliases=['roast'])
async def insult(context, *args):
    insults = open("data/insults.txt","r+", encoding="utf-8")

    if len(args):
        unluckyDude = args[0]
    else:
        userSet = context.message.channel.members
        unluckyDude = choice(userSet)
        while unluckyDude == context.me: unluckyDude = choice(userSet)
        unluckyDude = unluckyDude.mention
    lines = insults.readlines()
    chosen = choice(lines)
    response = ""
    for auto in chosen.split():
        if ord(auto[0]) not in range(ord('1'), ord('9') + 1): response += auto + " "
    await context.send(unluckyDude + " " + response)

@bot.event
async def on_message(message):
    if len(message.content.split()) > 0:
        if message.content.split()[0] == "changePrefix":
            if len(message.content.split()) == 1:
                bot.command_prefix = ''
            else:
                bot.command_prefix = message.content.split()[1]

    await bot.process_commands(message)

bot.run(TOKEN)
