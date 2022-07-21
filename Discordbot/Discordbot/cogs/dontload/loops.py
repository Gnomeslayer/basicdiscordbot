import sqlite3
import asyncio, json, http3, aiosqlite, sqlite3
from datetime import datetime
from discord.ext import commands, tasks
from discord.utils import get

 
class Loops(commands.Cog):

    def __init__(self, client):
        print("[Cog] Loops has been initiated")
        self.client = client
        self.autounmute.start()
        #print("Started the autounmute function with an interval of 10 seconds.")
        
    @commands.command(help='[Starts a given task.]')
    @commands.is_owner()
    async def start_task(self,ctx, *, mytask):
        if mytask == 'autounmute':
            await ctx.send("autounmute starting..")
            self.autounmute.start()

    @commands.command(help='[Stops a given task.]')
    @commands.is_owner()
    async def stop_task(self, ctx, *, mytask):
        if mytask == 'autounmute':
            await ctx.send("autounmute stopping..")
            self.autounmute.stop()

    @tasks.loop(seconds=300)
    async def autounmute(self):
        currtime = datetime.now()
        con = sqlite3.connect('bot.db')
        cur = con.cursor()
        for row in cur.execute("SELECT * FROM moderation WHERE active='Active'"):
            dbdate = datetime.fromisoformat(row[3])
            if dbdate <= currtime:
                targetGuild = self.client.get_guild(row[0])
                targetUser = get(self.client.get_all_members(), id=row[1])
                muterole = get(targetGuild.roles, name="Muted")
                await targetUser.remove_roles(muterole)
                await targetUser.send(f"You've been unmuted in the discord: {targetGuild}")
                #cur.execute('DELETE FROM moderation WHERE discordid=? AND userid=?', (row[0], row[1]))
                sql = ''' UPDATE moderation
                SET active = Inactive ,
                WHERE discordid = ? AND userid=?'''
                task = ("Inactive",row[0],row[1])
                cur.execute('UPDATE moderation SET active=? WHERE discordid=? AND userid=?', task)
                
        con.commit()
        con.close()
    
def setup(client):
    client.add_cog(Loops(client))
