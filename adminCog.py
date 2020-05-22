import discord, asyncio, os
import utils
from datetime import datetime
from discord.ext import commands

class AdminCommands(commands.Cog, name='Admin Commands'):


    def __init__(self, bot):
        self.bot = bot


    des__migrate = "Migrate all message history from one channel to another."

    @commands.command(name='migrate', brief=des__migrate, description=des__migrate)
    async def migrate(self, context):
        await context.send("Please send `!here` to target channel.")
        try:
            msg = await self.bot.wait_for('message', timeout=15.0, check=lambda msg: msg.author == context.author and msg.content.lower() == '!here')
        except asyncio.TimeoutError:
            await context.send('Operation aborted')
        else:
            channelMsg = []
            async for message in context.history(limit=999):
                channelMsg.append("`" + message.author.name + ":`\n" + message.content)
            for index in range(len(channelMsg) - 1, -1, -1):
                await msg.channel.send(channelMsg[index])
            

    des__emoji = "Copy all emojis of the current server to another."

    @commands.command(name='copyemojis', brief=des__emoji, description=des__emoji)
    async def getEmojis(self, context):
        emojis = context.guild.emojis
        await context.send("Please send `!here` to target guild.")
        try:
            msg = await self.bot.wait_for('message', timeout=15.0, check=lambda msg: msg.author == context.author and msg.content.lower() == '!here')
        except asyncio.TimeoutError:
            await context.send('Operation aborted')
        else:
            targetServer = msg.guild
            targetServerEmojis = [emoji.name for emoji in targetServer.emojis]
            newEmojis = 0
            for emoji in emojis:
                if emoji.name not in targetServerEmojis:
                    emote = await emoji.url.read()
                    await targetServer.create_custom_emoji(name=emoji.name, image=emote)
                    newEmojis += 1
            await context.send(str(newEmojis) + " new emojis added to this server from " + context.guild.name + " server.")