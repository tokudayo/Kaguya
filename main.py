import os, discord
from discord.ext import commands
from dotenv import load_dotenv
from codeforces import CodeforcesCommand
from general import GeneralPurpose


bot = commands.Bot(command_prefix='!', case_insensitive=True, description='Hi. Kaguya is a bot. Check out what Kaguya can do!')


@bot.event
async def on_message(message):

    # look for 'good bot' commendation
    if message.content.lower() == "good bot":
        if message.author.id==281411022881947654: await message.channel.send("Thank you, Master-sama.")
        else: await message.channel.send("Thank you.")

    # look for changePrefix [prefix]
    """
    if len(message.content.split()):
        if message.content.split()[0] == "changePrefix":
            if len(message.content.split()) == 1:
                bot.command_prefix = ''
            else:
                bot.command_prefix = message.content.split()[1]
    """
    await bot.process_commands(message)


@bot.event
async def on_ready():
    bot.add_cog(GeneralPurpose(bot))
    bot.add_cog(CodeforcesCommand(bot))
    print("Initialization completed.")


# Run the bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
