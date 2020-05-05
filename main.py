import os, discord
from discord.ext import commands
from dotenv import load_dotenv
from codeforces import CodeforcesUser
from webster import Word
from random import choice

load_dotenv()
encryptedToken = os.getenv('DISCORD_TOKEN')
TOKEN = ""
for c in encryptedToken: TOKEN += chr(ord(c) + 1)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Done")

@bot.command(name='insult', help='Roasts someone', aliases=['roast'])
async def insult(context, *args):
    insults = open("data/insults.txt","r+", encoding="utf-8")

    if len(args):
        unluckyDude = args[0]
        if context.me.mentioned_in(context.message):
            await context.send("Why would you try to do such thing to me?")
            return
        elif args[0][0] != '<' and args[0][1] != '@':
            await context.send("If you want to roast someone, do it like this: `" + bot.command_prefix + "roast [mention]` " +  "<:pathetic:707148847817687100>")
            return
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

@bot.command(name='info', help='Codeforces user info')
async def printInfo(context, *args):
    if (len(args) == 1):
        cfUser = CodeforcesUser(args[0])
        if not cfUser.isNULL:
            embed = discord.Embed(title="Codeforces user : " + cfUser.handle, color=0xff3729)
            embed.add_field(name="Country", value=cfUser.country, inline=True)
            embed.add_field(name="Rating", value=cfUser.rating, inline=True)
            embed.add_field(name="Rank", value=cfUser.rank, inline=True)
            embed.url = "https://codeforces.com/profile/" + cfUser.handle
            embed.set_thumbnail(url='https:' + cfUser.avatar)
            await context.send(embed=embed)
        else:
            await context.send("`User not found.`")
    else:
        await context.send("Info who? Try `!info [handle]` <:pathetic:707148847817687100>")

@bot.command(name='define')
async def dictLookup(context, *args):
    if (len(args)):
        embed = discord.Embed(title=args[0], color=0xb83f27)
        word = Word(args[0])
        defs = ""
        for auto in word.definition: defs += auto + '\n'
        embed.add_field(name="Definition: ", value=defs, inline=False)
        await context.send(embed=embed)
    else:
        await context.send("Missing one obvious argument: `!define [word to be defined]` <:pathetic:707148847817687100>")

@bot.event
async def on_message(message):
    if message.content.lower() == "good bot":
        if message.author.id==281411022881947654: await message.channel.send("Thank you, Master-sama.")
        else: await message.channel.send("Thank you.")

    if len(message.content.split()) > 0:
        if message.content.split()[0] == "changePrefix":
            if len(message.content.split()) == 1:
                bot.command_prefix = ''
            else:
                bot.command_prefix = message.content.split()[1]

    await bot.process_commands(message)

bot.run(TOKEN)
