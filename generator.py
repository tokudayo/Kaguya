import os, discord, random, asyncio
from discord.ext import commands

class GeneratorCommands(commands.Cog, name='Generator Commands'):


    def __init__(self, bot):
        self.bot = bot


    des__tree = "Generate a random tree containing V vertices"

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
                        temp += str(j + 1) + " " + prufer[i] + "\n" 
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

        random.seed()
        prufer = [random.randint(1, V) for x in range(V)]
        response = printTreeEdges(prufer, V)
        