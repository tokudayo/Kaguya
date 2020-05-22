import os, discord, random, asyncio
import utils
from discord.ext import commands

class GeneratorCommands(commands.Cog, name='Generator Commands'):


    def __init__(self, bot):
        self.bot = bot
        try:
            os.mkdir('output')
        except:
            pass


    des__tree = ("Generate a random tree containing V vertices from a random Prufer sequence. N should be smaller than 10000.\n")

    @commands.command(name='gentree', brief="Generate a random tree containing V vertices.", description=des__tree)
    async def genTree(self, context, V):

        def printTreeEdges(prufer, m):
            temp = ""
            vertices = m + 2
            vertex_set = [0] * vertices 
            for i in range(vertices - 2): 
                vertex_set[prufer[i] - 1] += 1
            j = 0
            for i in range(vertices - 2): 
                for j in range(vertices): 
                    if (vertex_set[j] == 0): 
                        vertex_set[j] = -1
                        temp += str(j + 1) + " " + str(prufer[i]) + "\n" 
                        vertex_set[prufer[i] - 1] -= 1
                        break
            
            j = 0
            for i in range(vertices): 
                if (vertex_set[i] == 0 and j == 0): 
                    temp += str(i + 1) + " "
                    j += 1
                elif (vertex_set[i] == 0 and j == 1): 
                    temp += str(i + 1)
            return temp

        try:
            V = int(V)
            if V <= 0:
                raise Exception("V must be > 0")
        except:
            await context.send("Invalid number of vertices.")
            return
        
        if V >= 30000:
            await context.send("Sorry, but it would take longer than you can ever wait. Queue cancelled.")
            return
        random.seed()
        prufer = [random.randint(1, V - 2) for x in range(V)]
        response = printTreeEdges(prufer, V - 2)
        if len(response) > 1990:
            PATH = 'output/genTree.txt'
            utils.dumpToFile(path=PATH, response=response)
            await context.send(file=discord.File(PATH))
        else:
            await context.send("```" + response + "```")


    des__array = "Generate an array of fixed length N. Elements range [L;R] can be specified. Array elements can be choosen to be distinct."

    @commands.command(name='genarray', brief='Generate an array of fixed length.', description=des__array)
    async def genArray(self, context, length, L = 0, R = 1000000000):
        length = int(length)
        L = int(L)
        R = int(R)
        random.seed()
        response = ""
        for _ in range(length):
             response += str(random.randint(L,R)) + " "
        if len(response) > 1975:
            utils.dumpToFile(response=response,path='output/randomArray.txt')
            await context.send(file=discord.File('output/randomArray.txt'))
        else:
            await context.send(response)


    des__perm = "Generate a permutation of N first positive integers."

    @commands.command(name='genperm', brief=des__perm, description=des__perm)
    async def genPerm(self, context, limit):
        limit = int(limit)
        random.seed()
        arr = []
        for posInt in range(limit): arr.append(posInt + 1)
        random.shuffle(arr)
        response = ""
        for elem in arr:
             response += str(elem) + " "
        if len(response) > 1975:
            utils.dumpToFile(response=response,path='output/randomArray.txt')
            await context.send(file=discord.File('output/randomArray.txt'))
        else:
            await context.send(response)