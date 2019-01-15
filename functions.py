import asyncio
import time

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
            await ctx.send("""
Are you sure this is a correct log? 
https://www.warcraftlogs.com/reports/wfz4BZJhYa98VK32/#fight=last&type=healing is an example log. The text following the "#" is optional text that some logs may have.""")