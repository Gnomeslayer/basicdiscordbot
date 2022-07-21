import discord,sqlite3, re
from datetime import datetime, timedelta
from io import BytesIO
from discord.ext import commands
from discord.utils import get

 
class Reminder(commands.Cog):

    def __init__(self, client):
        print("[Cog] Reminder has been initiated")
        self.client = client
        self.con = sqlite3.connect('bot.db')
        self.cur = self.con.cursor()
            #
            #con.commit()
            #con.close()


    @commands.command(help='[Remind you to do something]')
    async def remindme(self, ctx, whattime, *, message):
        mynumbers = re.findall(r'\d+', whattime)
        for i in mynumbers:
            whattime = whattime.replace(str(i), '')
            days = 0
            hours = 0
            minutes = 0
            seconds = 0
            i = 0
            mything = list(whattime)
            while i in range(len(mynumbers)):
                #days to seconds
                if mything[i] == 'd' or mything[i] == 'D':
                    days = mynumbers[i]
                #hours to seconds
                if mything[i] == 'h' or mything[i] == 'H':
                    hours = mynumbers[i]
                #minutes to seconds
                if mything[i] == 'm' or mything[i] == 'M':
                    minutes = mynumbers[i]
                if mything[i] == 's' or mything[i] == 'S':
                    seconds = mynumbers[i]
                i+= 1

            reminddate = datetime.now() + timedelta(days=int(days),hours=int(hours),minutes=int(minutes),seconds=int(seconds))
            discordid = ctx.guild.id
            memberid = ctx.author.id
            membermention = ctx.author.mention
            active = "Active"
            self.cur.execute("INSERT INTO reminder VALUES (?,?,?,?,?,?)", (discordid,memberid,membermention,reminddate,message,active))
            self.con.commit()

    @commands.command(help='[Reminds someone to do something]')
    async def remind(self, ctx, member: discord.Member, whattime, *, message):
        mynumbers = re.findall(r'\d+', whattime)
        for i in mynumbers:
            whattime = whattime.replace(str(i), '')
            days = 0
            hours = 0
            minutes = 0
            seconds = 0
            i = 0
            mything = list(whattime)
            while i in range(len(mynumbers)):
                #days to seconds
                if mything[i] == 'd' or mything[i] == 'D':
                    days = mynumbers[i]
                #hours to seconds
                if mything[i] == 'h' or mything[i] == 'H':
                    hours = mynumbers[i]
                #minutes to seconds
                if mything[i] == 'm' or mything[i] == 'M':
                    minutes = mynumbers[i]
                if mything[i] == 's' or mything[i] == 'S':
                    seconds = mynumbers[i]
                i+= 1

            reminddate = datetime.now() + timedelta(days=int(days),hours=int(hours),minutes=int(minutes),seconds=int(seconds))
            discordid = ctx.guild.id
            memberid = member.id
            membermention = member.mention
            active = "Active"
            self.cur.execute("INSERT INTO reminder VALUES (?,?,?,?,?,?)", (discordid,memberid,membermention,reminddate,message,active))
            self.con.commit()

    @commands.command(help='[Deletes a reminder]')
    async def delmyreminder(self, ctx, remindernumber):
        pass

    @commands.command(help='[sends the list of reminders from author.]')
    async def reminderlist(self, ctx):
        authorid = ctx.author.id
        discordid = ctx.guild.id
        userAvatar = ctx.author.avatar.url
        embed = discord.Embed(timestamp = ctx.message.created_at)
        embed.set_author(name = f'Reminder list for {ctx.author}')
        embed.set_footer(text = f'Requested by {ctx.author}', icon_url=userAvatar)
        for row in self.cur.execute("SELECT * FROM reminder WHERE memberid=:authorid AND active='Active' AND discordid=:discordid", {"discordid": discordid, "authorid": authorid}):
            embed.add_field(name=f"Date of reminder: {row[3]}", value=f"{row[4]}", inline="False")
        await ctx.author.send(embed=embed)

    @commands.command(help='[Shows ALL reminders for ALL users]')
    async def allreminders(self, ctx):
        discordid = ctx.guild.id
        userAvatar = ctx.author.avatar.url
        content = ''
        targetGuild = self.client.get_guild(ctx.guild)
        mystring = ''
        for row in self.cur.execute("SELECT * FROM reminder WHERE active='Active' AND discordid=:discordid", {"discordid": discordid}):
            
            targetUser = get(self.client.get_all_members(), id=row[1])
            mystring += f"Reminder for {targetUser} - Date of reminder: {row[3]}\n**REMINDER** - {row[4]}\n"
            
        as_bytes = map(str.encode, mystring)
        content = b''.join(as_bytes)
        await ctx.author.send("List of all reminders", file=discord.File(BytesIO(content), "allreminders.txt"))
            
def setup(client):
    client.add_cog(Reminder(client))