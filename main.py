import os, discord
from discord.ext import commands
from dotenv import load_dotenv
from codeforces import CodeforcesCommand
from general import GeneralPurpose


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


load_dotenv()
encryptedToken = os.getenv('DISCORD_TOKEN')
TOKEN = ""
for c in encryptedToken: TOKEN += chr(ord(c) + 1)
bot = commands.Bot(command_prefix='!')
bot.run(TOKEN)
