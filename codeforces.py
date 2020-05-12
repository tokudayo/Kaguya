import requests, json, discord, random, asyncio, os
import output
from datetime import datetime
from discord.ext import commands
from matplotlib import pyplot as plt
from tabulate import tabulate

class CodeforcesUser:


    def __init__(self, query):
        self.handle = ""
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
            """ extend the rating data to current date.
            if len(ratingData):
                self.ratingChange.append([int(datetime.timestamp(datetime.now())), ratingData[len(ratingData) - 1]['newRating']])
            """
            jsonData = rawData.json()
        else:
            self.isNULL = True



class CodeforcesProblem:


    def __init__(self, data):
        self.contestId = ""
        self.index = ""
        self.rating = 0

        self.name = data['name']
        self.tags = data['tags']
        if 'rating' in data: self.rating = data['rating']
        if 'solvedCount' in data: self.solvedCount = data['solvedCount']
        if 'contestId' in data and 'index' in data:
            self.contestId = data['contestId']
            self.index = data['index']
            self.url = "https://codeforces.com/problemset/problem/" + str(self.contestId) + "/" + self.index
            self.shortName = str(self.contestId) + self.index
        else:
            self.url = ""



class CodeforcesCommand(commands.Cog, name='Codeforces Commands'):


    def __init__(self, bot):
        self.bot = bot
        self.loadProblems()
        try:
            os.mkdir('cf__output')
        except:
            pass

    def loadProblems(self):
        self.problems = []
        url = "https://codeforces.com/api/problemset.problems?tags="
        rawData = requests.get(url)
        jsonData = rawData.json()
        if jsonData['status'] == 'OK':
            data = jsonData['result']
            problemsDat = data['problems']
            problemStat = data['problemStatistics']
            for index in range(0,len(problemsDat)): 
                problem = problemsDat[index]
                problem['solvedCount'] = problemStat[index]['solvedCount']
                self.problems.append(CodeforcesProblem(problem))
            return 'OK'
        else:
            return 'ERROR'


    des__info = "Codeforces user info look-up."

    @commands.command(name='cfinfo', brief=des__info, description=des__info)
    async def printInfo(self, context, handle=""):
        if (handle):
            cfUser = CodeforcesUser(handle)
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


    des__rating = "Draw a rating graph of Codeforces user(s)."

    @commands.command(name='cfrating', brief=des__rating, description=des__rating)
    async def ratingGraph(self, context, *users):
        if (len(users)):
            plt.figure()
            plt.ylabel('Rating')
            plt.xlabel('Time')
            title = "Rating of "
            for auto in users:
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
            plt.savefig('cf__output/ratingPlot.png')
            await context.send(file=discord.File('cf__output/ratingPlot.png'))
        else:
            await context.send("Rating of whom? Try `!rating [list of user(s)]` <:pathetic:707148847817687100>")


    des__load = "Load the lastest of Codeforces official problems database."

    @commands.command(name='cfload', brief=des__load, description=des__load)
    async def problemUpdate(self, context):
        if self.loadProblems() == 'OK':
            await context.send(f"Data of {str(len(self.problems))} problems loaded.")
        else:
            context.send("Unexpected error occured while connecting to Codeforces' API server.")


    problemTags = ['data_structures', 'implementation', 'brute_force', 'math', 'dfs_and_similar', 'graphs', 'greedy', 'dp', 'binary_search', 'constructive_algorithms', 'sortings', 'strings', 'matrices', 'trees', 'dsu', 'number_theory', 'shortest_paths', 'two_pointers', 'bitmasks', 'combinatorics', 'fft', 'hashing', 'interactive', 'probabilities', 'divide_and_conquer', 'games', 'geometry', 'string_suffix_structures', 'meet-in-the-middle', 'ternary_search', 'flows', 'expression_parsing', '*special', 'graph_matchings', 'chinese_remainder_theorem', '2-sat', 'schedules']
    
    des__problem = ("Return information of problems having specified tags.\n"
                    "Available tags are:\n")

    for tag in problemTags: des__problem += tag + "  "

    @commands.command(name='cfproblem', brief='Codeforces problems query.', description=des__problem)
    async def problemQuery(self, context, *tags):

        def outputDump(entries):
            responseData = []
            for problem in entries:
                responseData.append([problem.shortName, problem.name, problem.rating, problem.solvedCount])
            responseData.sort(key=lambda x : x[2]) # Rating column
            response = tabulate(responseData, headers=['ID', 'Problem name', 'Difficulty', 'Solved'], tablefmt='orgtbl')
            return response

        if len(tags):
            query = []
            for auto in tags:
                new = ""
                for char in auto:
                    if char=="_": new += " "
                    else: new += char.lower()
                query.append(new)
            query = set(query)
            entries = []
            for problem in self.problems:
                if query.issubset(set(problem.tags)):
                    entries.append(problem)
            # to be fixed
            if len(entries):
                msg = await context.send(
                    f"```Found {str(len(entries))} entries.\n"
                    f"Filter by difficulty?```"
                )
                await msg.add_reaction('👍')
                await msg.add_reaction('👎')
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=lambda reaction, user: user == context.author and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎'))
                except asyncio.TimeoutError:
                    await context.send("Operation cancelled.")
                else:
                    if str(reaction.emoji) == '👍':
                        await context.send('Enter difficulty range (e.g. 1700 2000)')
                        try:
                            msg = await self.bot.wait_for('message', timeout=15.0, check=lambda msg: msg.author == user)
                        except asyncio.TimeoutError:
                            await context.send('No?')
                        else:
                            msg = msg.content
                            try:
                                entriesByDif = []
                                LO = int(msg.split()[0])
                                HI = int(msg.split()[1])
                                if (LO > HI): raise Exception("LO > HI")
                            except:
                                await context.send("Invalid range")
                                return
                            
                            for problem in entries:
                                if problem.rating and LO <= problem.rating <=  HI:
                                    entriesByDif.append(problem)
                            response = outputDump(entriesByDif)
                            if len(response) < 1950:
                                await context.send(f"Found {str(len(entriesByDif))} entries.\n" + "```" + response + "```")
                            else:
                                await context.send("Data length exceeds Discord limit. Dumping to text file.")
                                PATH = 'output/problemQuery.txt'
                                output.dumpToFile(path= PATH, response=response)
                                await context.send(file=discord.File(PATH))
                    else:
                        await context.send(f"No? Here is the list of {len(entries)} problems, sorted by difficulty.")
                        response = outputDump(entries)
                        if len(response) > 1950:
                            PATH = 'output/problemQuery.txt'
                            output.dumpToFile(path= PATH, response=response)
                            await context.send(file=discord.File(PATH))
                        else:
                            await context.send("```" + response + "```")

            else:
                await context.send("No entries found.")

        else:
            await context.send("Please specify the tag(s) of problems. Try `!problem [list of tags]`")