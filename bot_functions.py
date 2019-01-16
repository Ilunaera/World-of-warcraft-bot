import asyncio
import time
import math
import json
import requests

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
        parts = loglink.split('/')
        if parts[4]:
            r_id_split = parts[4].split('#')
            r_id = r_id_split[0]
            out = '!wf l ' + r_id + ' -d ' + str(death_thresh)
            linksend = await ctx.send(out)
            time.sleep(5)
            await linksend.delete()

        else:
            await ctx.send(""" Are you sure this is a correct log? 
            https://www.warcraftlogs.com/reports/wfz4BZJhYa98VK32/#fight=last&type=healing is an example log. 
            The text following the "#" is optional text that some logs may have.""")

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

    