import asyncio
import time
import math
import json
import requests
import myToken

async def logsplit(ctx, loglink):
    parts = loglink.split('/')
    try:
        if parts[4]:
            r_id_split = parts[4].split('#')
            r_id = r_id_split[0]
            return r_id
    except IndexError:
        return False
        
async def bot_ready(bot):
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

async def livelog(ctx, loglink='', death_thresh = '0', content='Please enter a character name and fightstyle. For example, .live <link> <death_threshold>'):
    if loglink == '':
         await ctx.send('''Use the command like this: 
            ```.live <log link> [DeathThreshold]``` 
        though the death threshold is an optional parameter.''')
    else:
                r_id = await logsplit(ctx, loglink)
                if r_id is not False:
                    out = '!wf l ' + r_id + ' -d ' + str(death_thresh)
                    linksend = await ctx.send(out)
                    time.sleep(5)
                    await linksend.delete()
                else:
                    await ctx.send("Invalid link given.")

async def get_affixes(ctx):
    response = requests.get("https://raider.io/api/v1/mythic-plus/affixes?region=eu&locale=en")
    affixes = json.loads(response.text)
    affix_list = affixes["title"]
    await ctx.send(affix_list)

async def get_progression(ctx, name, realm):
    response = requests.get("https://raider.io/api/v1/characters/profile?region=eu&realm="+realm+"&name=" + name +"&fields=raid_progression%2Cmythic_plus_scores")
    get_info = json.loads(response.text)
    hc_killed = get_info['raid_progression']
    kill_prog = ""
    name = name.capitalize()
    progress = "Showing progress for " + name + ":"
    await ctx.send(progress)
    for i in hc_killed:
        title_split = i.split("-")
        new_title = ""
        for x in title_split:
            new_title = new_title + x.capitalize() + " "
        summ = hc_killed[i]["summary"]
        kill_prog = kill_prog + new_title + " - " + summ + "\n"

    mythic_scores = "Raider IO Mythic+ Score: " + str(math.floor(get_info["mythic_plus_scores"]["all"])) + "\n"
    await ctx.send(mythic_scores)
    await ctx.send(kill_prog)

async def attendance(ctx,loglink):
    r_id = await logsplit(ctx, loglink)
    if r_id is not False:
        response = requests.get("https://www.warcraftlogs.com/v1/report/fights/"+r_id+"?api_key="+ myToken.getWCLKey())
        get_info = json.loads(response.text)
        friendlies = get_info["friendlies"]
        friendly_fighters = ""

        for i in friendlies:
            friendly_fighters= friendly_fighters + i["name"] + " has been involved in "
            fights = len(i["fights"])
            friendly_fighters = friendly_fighters + str(fights) + " fights! \n"
        await ctx.send(friendly_fighters)