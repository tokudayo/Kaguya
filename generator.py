import os, discord, random, asyncio
import output
from discord.ext import commands

class GeneratorCommands(commands.Cog, name='Generator Commands'):


    def __init__(self, bot):
        self.bot = bot
        try:
            os.mkdir('output')
        except:
            pass


    des__tree = "Generate a random tree containing V vertices from a random Prufer sequence. N should be smaller than 10000."

    @commands.command(name='gentree', brief=des__tree, description=des__tree)
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
        except:
            await context.send("Invalid number of vertices.")
        
        random.seed()
        prufer = [random.randint(1, V - 2) for x in range(V)]
        response = printTreeEdges(prufer, V - 2)
        if len(response) > 1990:
            PATH = 'output/genTree.txt'
            output.dumpToFile(path=PATH, response=response)
            await context.send(file=discord.File(PATH))
        else:
            await context.send("```" + response + "```")