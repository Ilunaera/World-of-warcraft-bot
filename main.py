import discord
from discord.ext import commands
import time
import signal
import bot_functions
import myToken

#I have added this - though it may be unnecessary - due to the program taking a long time to interrupt. 
signal.signal(signal.SIGINT, signal.SIG_DFL)

description = '''This bot is made to aid people who may struggle with command line interfaces for various bots. In some
cases the bot may trigger what response you would help - for example, the .live command will output directly into wipefest
bot. With Raidbots, that is not the case.'''

bot = commands.Bot(command_prefix='.', description=description, case_insensitive=True,pm_help=True)

@bot.event
async def on_ready():
    await bot_functions.bot_ready(bot)

@bot.event
async def on_message(message):
    # Everytime a log is linked, wipefest pipes up - I don't like it, so I removed it. 
    # Make sure your bot has manage messages for this to work.
    if 'See this fight on Wipefest' in message.content:
        await message.delete()
    await bot.process_commands(message)

@bot.command(name="live", alias=['livelog', 'llog'])
async def live(ctx, loglink='', death_thresh = '0', content=description):
    """.live <loglink> <*Death Threshold> - Splits the log up to get the ID, then sends it to wipefest bot. """
    await bot_functions.livelog(ctx, loglink, death_thresh, content)

@bot.command(name="affixes", aliases=['affix'])
async def affixes(ctx):
    """.affixes - Gets list of affixes."""
    await bot_functions.get_affixes(ctx)

@bot.command(name="progress", aliases=['lookup', 'character','scores'])
async def progress(ctx,name, realm):
    """.progress <name> <realm> - Return M+ Score + Raid Progression."""
    await bot_functions.get_progression(ctx,name, realm)
    
@bot.command()
async def attend(ctx, loglink):
    """.attend <log> = Who showed up?"""
    await bot_functions.attendance(ctx, loglink)

bot.run(myToken.return_token())