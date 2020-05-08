import requests, json, discord
from datetime import datetime
from discord.ext import commands
from matplotlib import pyplot as plt

class CodeforcesUser:


    def __init__(self, query):
        self.handle = ""
        self.isNULL = True
        self.rating = 0
        self.rank = "No rank"
        self.country = "Unknown"
        self.avatar = ""
        self.ratingChange = []

        # Get date from Codeforces API and process
        url = "https://codeforces.com/api/user.info?handles=" + query
        rawData = requests.get(url)
        jsonData = rawData.json()
        if jsonData['status'] == 'OK':
            data = jsonData['result']
            data = data[0]
            self.isNULL = False
            self.handle = data['handle']
            if 'rating' in data: self.rating = data['rating']
            if 'rank' in data: self.rank = data['rank']
            self.avatar = data['avatar']
            if 'country' in data: self.country = data['country']
            rawData = requests.get("https://codeforces.com/api/user.rating?handle=" + self.handle)
            ratingData = rawData.json()['result']
            for auto in ratingData:
                self.ratingChange.append((auto['ratingUpdateTimeSeconds'],auto['newRating']))
            if len(ratingData):
                self.ratingChange.append([int(datetime.timestamp(datetime.now())), ratingData[len(ratingData) - 1]['newRating']])
            jsonData = rawData.json()



class CodeforcesProblem:


    def __init__(self, data):
        self.contestId = ""
        self.problemsetName = ""
        self.index = ""

        for key in data:
            self.key = data[key]
        if 'contestId' in data and 'problemsetName' in data and 'index' in data:
            self.url = "https://codeforces.com/problemset/problem/" + str(self.contestId) + "/" + self.index
        else:
            self.url = ""



class CodeforcesCommand(commands.Cog, name='Codeforces Commands'):


    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='info', help='Codeforces user info look-up.')
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


    @commands.command(name='rating', help='Draw a rating graph of Codeforces user(s).')
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


    @commands.command(name='problem', help='Information regarding Codeforces problems with specific attributes.')
    async def problemQuery(self, context, *args):
        if len(args):
            query = ""
            for auto in args[:len(args) - 1]: query += auto + ";"
            query += args[len(args) - 1]
            url = "https://codeforces.com/api/problemset.problems?tags="
            rawData = requests.get(url + query)
            jsonData = rawData.json()
            if jsonData['status'] == 'OK':
                data = jsonData['result']
                problems = data['problems']
                # problemStats = data['problemStatistics']
                await context.send(str(len(problems)) +  " entries found.")
        else:
            await context.send("Please specify the tag(s) of problems. Try `!problem [list of tags]`")