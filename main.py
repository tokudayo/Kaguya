import os, discord
from discord.ext import commands
from dotenv import load_dotenv
from codeforces import CodeforcesUser
from webster import Word
from wiki import WikiPage
from random import choice
from datetime import datetime
from matplotlib import pyplot as plt

load_dotenv()
encryptedToken = os.getenv('DISCORD_TOKEN')
TOKEN = ""
for c in encryptedToken: TOKEN += chr(ord(c) + 1)

bot = commands.Bot(command_prefix='!')

class GeneralPurpose(commands.Cog, name='General Commands'):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='insult', help='Roasts someone', aliases=['roast'])
    async def insult(self, context, *args):
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

class CodeforcesCommand(commands.Cog, name='Codeforces Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info', help='Codeforces user info')
    async def printInfo(self, context, *args):
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

    @commands.command(name='rating', help='Codeforces user info')
    async def ratingGraph(self, context, *args):
        if (len(args)):
            plt.figure()
            plt.ylabel('Rating')
            plt.xlabel('Time')
            title = "Rating of "
            for auto in args:
                cfUser = CodeforcesUser(auto)
                if not cfUser.isNULL and len(cfUser.ratingChange) > 0:
                    title += cfUser.handle + " "
                    plt.plot([x[0] for x in cfUser.ratingChange], [x[1] for x in cfUser.ratingChange], label=cfUser.handle)
                    plt.legend()
            tick = plt.xticks()
            labels = []
            for auto in tick[0]:
                T = datetime.fromtimestamp(auto)
                labels.append(str(int(T.month)) + "/" + str(int(T.year)))
                
            plt.xticks(ticks = tick[0], labels=labels)
            if title == "Rating of ": title += "no one."
            plt.title(title)
            plt.savefig('plot.png')
            await context.send(file=discord.File('plot.png'))
        else:
            await context.send("Rating of whom? Try `!rating [list of user(s)]` <:pathetic:707148847817687100>")

@bot.command(name='define')
async def dictLookup(context, *args):
    if (len(args)):
        lookup = ""
        for auto in args: lookup += auto + " "
        word = Word(lookup)
        if word.isNULL:
            await context.send("Sorry, can't seem to find the word.")
        else:
            if word.redirected: await context.send("I can't find the word. Showing definition for:")
            embed = discord.Embed(title=word.word, color=0xb83f27)
            if len(word.definition) == 0:
                embed.add_field(name="\u200b", value="No definition", inline=False)
            else:
                temp = ""
                for auto in word.definition[0:min(5,len(word.definition))]:
                    temp += auto + '\n'
                embed.add_field(name='Definition:', value=temp, inline=False)
                index = 5
                temp = ""
                while index < len(word.definition):
                    temp += word.definition[index] + '\n'
                    if (index+1) % 5 == 0 or index == len(word.definition)-1:
                        embed.add_field(name="\u200b ", value=temp, inline=False)
                        temp = ""
                    index += 1
                        
            await context.send(embed=embed)
    else:
        await context.send("Missing one obvious argument: `!define [word to be defined]` <:pathetic:707148847817687100>")

@bot.command(name='wiki')
async def wikiLookup(context, *args):
    if (len(args)):
        wikiPage = WikiPage(args)
        embed = discord.Embed(title=wikiPage.title, color=0xb83f27)
        embed.url = wikiPage.url
        if wikiPage.title != "No article found." and wikiPage.title != "Topic too broad.":
            embed.add_field(name='Summary:',value=wikiPage.shortSummary)
        await context.send(embed=embed)
    else:
        await context.send("Missing one obvious argument: `!wiki [subject]` <:pathetic:707148847817687100>")

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

@bot.event
async def on_ready():
    bot.add_cog(GeneralPurpose(bot))
    bot.add_cog(CodeforcesCommand(bot))
    print("Done")

bot.run(TOKEN)

