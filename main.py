import discord
from discord.ext import commands
import time
import signal
import functions
import myToken

#I have added this - though it may be unnecessary - due to the program taking a long time to interrupt. 
signal.signal(signal.SIGINT, signal.SIG_DFL)

description = '''This bot is made to aid people who may struggle with command line interfaces for various bots. In some
cases the bot may trigger what response you would help - for example, the .live command will output directly into wipefest
bot. With Raidbots, that is not the case.'''
bot = commands.Bot(command_prefix='.', description=description)
client = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    #Everytime a log is linked, wipefest pipes up - I don't like it, so I removed it. 
    #Make sure your bot has manage messages for this to work.
    if 'See this fight on Wipefest' in message.content:
        await message.delete()
    await bot.process_commands(message)

@bot.command()
async def live(ctx, loglink='', death_thresh = '0', content='Please enter a character name and fightstyle. For example, .live <link> <death_threshold>'):
    """Splits the log up to get the ID, then sends it to wipefest bot. """
    await functions.livelog(ctx, loglink, death_thresh, content)

bot.run(myToken.return_token())