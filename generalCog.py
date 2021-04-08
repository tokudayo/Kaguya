import discord, random, asyncio, utils
from discord.ext import commands
from webster import Word
from wiki import WikiPage
from random import choice

class GeneralPurpose(commands.Cog, name='General Commands'):
    
    
    def loadResponse(self):
        self.response = []
        res = open("data/insults.txt","r+", encoding="utf-8")
        data = res.readline()
        trigger = True
        res = []
        for line in data:
            if trigger:
                res = [line]
                trigger = False
            else:
                res.append(line)
                self.response.append(res)
                trigger = True

    
    def __init__(self, bot):
        self.bot = bot
        self.loadResponse()


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


    des__rand = "Generate a random number between 1 and 100."

    @commands.command(name='roll', brief=des__rand, description=des__rand)
    async def randomNum(self, context):
        random.seed()
        await context.send(str(random.randint(1,100)))


    des__calc = "Calculate a simple arithmetic expression."

    @commands.command(name='calc', brief=des__calc, description=des__calc)
    async def calc(self, context, *args):
        check = True
        expression = ""
        for auto in args:
            expression += auto
        for auto in expression:
            if 'a' < auto < 'z':
                check = False
                break
        if check:
            response = str(eval(expression))
            await context.send(response)

    '''
    des__learn = "Teach me to response to a certain phrase."

    @commands.command(name='learn', brief=des__learn, description=des__learn)
    async def learnResponse(self, context, *args):
        trigger = ""
        response = ""
        await context.send("What phrase do you want me to response to?")
        try:
            msg = await self.bot.wait_for('message', timeout=15.0, check=lambda msg: msg.author == context.message.author)
        except asyncio.TimeoutError:
            await context.send('No?')
        else:
            trigger = msg.content
            await context.send("What should i response to that?")
            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=lambda msg: msg.author == context.message.author)
            except asyncio.TimeoutError:
                await context.send('No?')
            else:
                response = msg.content
        if trigger != "" and response != "":
            this.response.append([trigger, response])\
    '''

    des__jap = "Hiragana/Katakana to Romaji translation practice."

    @commands.command(name='jprac', brief=des__jap, description=des__jap)
    async def japanesePrac(self, context, *args):
        hiragana = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわを"
        katakana = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲ"
        romaji = ["a", "i", "u", "e", "o", "ka", "ki", "ku", "ke", "ko", "sa", "shi", "su", "se", "so",
                 "ta", "chi", "tsu", "te", "to", 'na',  'ni', 'nu', 'ne', 'no', 'ha', 'hi', 'fu', 'he',
                 'ho', 'ma', 'mi', 'mu', 'me', 'mo', 'ya', 'yu', 'yo', 'ra', 'ri', 'ru', 're', 'ro',
                 'wa', 'wo']
        questBank = []
        if len(args):
            if args[0] == 'k': questBank += katakana
            elif args[0] == 'h': questBank += hiragana
            else: questBank += random.choice([hiragana, katakana])
        else:
            questBank += random.choice([hiragana, katakana])

        wordLen = random.randint(1, 5)
        quest = ""
        ans = ""
        for _ in range(wordLen):
            letterIndex = random.choice(range(len(romaji)))
            quest += questBank[letterIndex]
            ans += romaji[letterIndex]


        await context.send(quest)
        try:
            msg = await self.bot.wait_for('message', timeout=10.0, check=lambda msg: msg.author == context.author)
        except asyncio.TimeoutError:
            await context.send('The answer is: ' + ans)
        else:
            if (msg.content.strip().lower() == ans):
                await context.send('Correct.')
            else:
                await context.send('Wrong answer.\nCorrect answer: ' + ans)
