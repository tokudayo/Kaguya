import discord, asyncio

def dumpToFile(**kwargs):
    f = open(kwargs['path'],'w+', encoding='utf-8')
    f.write(kwargs['response'])
    f.close()

async def yesnoReact(context, message):
    msg = await context.send(message)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')
    try:
        reaction, user = await context.bot.wait_for('reaction_add', timeout=15.0, check=lambda reaction, user: user == context.author and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎'))
    except asyncio.TimeoutError:
        return "TIMEOUT"
    else:
        return {
            'reaction': reaction,
            'user': user,
        }