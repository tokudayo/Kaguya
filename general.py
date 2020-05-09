import discord
from discord.ext import commands
from webster import Word
from wiki import WikiPage
from random import choice

class GeneralPurpose(commands.Cog, name='General Commands'):
    

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='insult', help='Roasts a random dude or a specific person.', aliases=['roast'])
    async def insult(self, context, *args):
        insults = open("data/insults.txt","r+", encoding="utf-8")
        if len(args):
            unluckyDude = args[0]
            if context.me.mentioned_in(context.message):
                await context.send("Why would you try to do such thing to me?")
                return
            elif args[0][0] != '<' and args[0][1] != '@':
                await context.send("If you want to roast someone, do it like this: `" + self.bot.command_prefix + "roast [mention]` " +  "<:pathetic:707148847817687100>")
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


    @commands.command(name='define', help='Word look-up in English-English Merriam-Webster dictionary.')
    async def dictLookup(self, context, *args):
        if (len(args)):
            lookup = ""
            for auto in args: lookup += auto + " "
            word = Word(lookup)
            if word.isNULL:
                await context.send("Sorry, can't seem to find the word.")
            else:
                if word.redirected: await context.send("I can't find the word. Showing definition for:")
                embed = discord.Embed(title=word.word, color=0xb83f27)
                embed.set_author(name="")
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


    @commands.command(name='wiki', help='Shows Wikipedia summary for a topic.')
    async def wikiLookup(self, context, *args):
        if (len(args)):
            wikiPage = WikiPage(args)
            embed = discord.Embed(title=wikiPage.title, color=0xb83f27)
            embed.set_author(name="")
            embed.url = wikiPage.url
            if wikiPage.title != "No article found." and wikiPage.title != "Topic too broad.":
                embed.add_field(name='Summary:',value=wikiPage.shortSummary)
            await context.send(embed=embed)
        else:
            await context.send("Missing one obvious argument: `!wiki [topic]` <:pathetic:707148847817687100>")