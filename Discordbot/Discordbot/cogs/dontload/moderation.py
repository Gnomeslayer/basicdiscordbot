import discord, asyncio, sqlite3
from datetime import datetime, timedelta
from io import BytesIO
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
 
class Moderation(commands.Cog):

    def __init__(self, client):
        print("[Cog] Moderation has been initiated")
        self.client = client

    @commands.command()
    async def getchans(self, ctx):
        await ctx.send(ctx.channel.guild.id)

    #Kicks/Bans everybody who has an account less than 1 day old or who has joined within 24 hours.
    @commands.command(help='[Stops a raid]',aliases=['raid','raiddefense'])
    @commands.has_any_role('bot','Bot','Owner')
    async def raid_defense(self,ctx):
        memberslist = []
        memberslist_string = ''
        guildid = ctx.guild
        if ctx.channel.name == 'botstuff':
            for i in bot.guilds:
                for member in i.members:
                    if member.id != 832106800580001813:
                        if guildid == member.guild:
                            joineddate = datetime.now() - member.joined_at
                            createddate = datetime.now() - member.created_at
                            if joineddate.days <= 1 or createddate.days <= 1:
                                mymembers = {
                                    'Member name:': member,
                                    'Member id:': member.id,
                                    'Member roles:': member.roles,
                                    'Created:': member.created_at,
                                    'Joined:': member.joined_at
                                    }
                                memberslist.append(mymembers)
                                await member.send('Kicked due to anti-raid procedures. If you believe this is in error, feel free to rejoin the discord. You are not banned.')
                                await member.send(discord.abc.GuildChannel.create_invite(ctx.message.channel,max_uses=0,max_age=0))
                                await member.kick()

            await ctx.send('I have compiled a list of members who were kicked. Please note this list is only sent to help verify everybody who should have been kicked. \nI only check for accounts created or joined within the last 24 hours.')
            for i in memberslist:
                for a,b in i.items():
                    memberslist_string += (f'{a} : {b} \n')

                memberslist_string += ('\n')
            as_bytes = map(str.encode, memberslist_string)
            content = b''.join(as_bytes)
            await ctx.send("Raid List", file=discord.File(BytesIO(content), "raidlist.txt"))

    @commands.command(help='[Deletes # messages in a channel.]')
    @commands.has_any_role('bot','Bot','Owner')
    async def clear(self,ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        msg = await ctx.channel.send(f'```\nCleared {amount} message(s) from chat channel. ```')
        await msg.delete(delay=2)

    @commands.command(help='[Kicks the mentioned user.]')
    @commands.has_any_role('bot','Bot','Owner')
    async def kick(self,ctx, member : discord.Member, *, reason = None):
        if reason == None:
            reason = "No reason given."
            await member.kick(reason=reason)

    @commands.command(help='[Bans the mentioned user.]')
    @commands.has_permissions(ban_members =True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        if reason == None:
            reason = "No reason given."
        if ctx.author.top_role > member.top_role:
            guild = ctx.guild
            await guild.ban(member, reason=reason)
        elif ctx.author.top_role < member.top_role:
            await ctx.send(f"I'm sorry {ctx.author.mention}, but I cannot ban someone who is better than you.")
        elif ctx.author.top_role == member.top_role:
            await ctx.send(f"I'm sorry {ctx.author.mention}, your roles match and according to article 32, subsection 193, paragraph 3, dotpoint 8, I can't ban him")
        else:
            await ctx.send("Can't ban. Soz bro.")
            
            
    @commands.command(help='[Unbans the mentioned user.]')
    @commands.has_any_role('bot','Bot','Owner')
    async def unban(self,ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
                return


    @commands.command(help='[Mutes someone.]')
    @commands.has_any_role('bot','Bot','Owner')
    async def mute(self, ctx, member: discord.Member):
        senderrole = ctx.author.roles
        targetrole = member.roles
        guildroles = ctx.guild.roles
        muterole = get(ctx.guild.roles, name="Muted")
        senderroleindex = 0
        targetroleindex = 0
        for i in guildroles:
            for a in senderrole:
                if a == i:
                    if senderroleindex < guildroles.index(i):
                        senderroleindex = guildroles.index(i)
            for a in targetrole:
                if a == i:
                    if targetroleindex < guildroles.index(i):
                        targetroleindex = guildroles.index(i)

        if senderroleindex > targetroleindex:
            await ctx.send(f"Muted: {member.mention}")
            await member.add_roles(muterole)
        elif senderroleindex == targetroleindex or senderroleindex < targetroleindex:
            await ctx.send("Cannot mute someone with the same or greater role than you.")

    @commands.command(help='[Unmutes someone.]')
    @commands.has_any_role('bot','Bot','Owner')
    async def unmute(self, ctx, member: discord.Member):
        muterole = get(ctx.guild.roles, name="Muted")
        await member.remove_roles(muterole)
        await ctx.send(f"Unmuted {member.mention}")
        await member.send(f"You've been unmuted in the discord {ctx.guild.name}")

    @commands.command(help='[Temporarily mutes someone. Default length is 60 seconds.]')
    @commands.has_any_role('bot','Bot','Owner')
    async def tempmute(self, ctx,  member : discord.Member, length = 60):
        senderrole = ctx.author.roles
        targetrole = member.roles
        guildroles = ctx.guild.roles
        muterole = get(ctx.guild.roles, name="Muted")
        senderroleindex = 0
        targetroleindex = 0
        for i in guildroles:
            for a in senderrole:
                if a == i:
                    if senderroleindex < guildroles.index(i):
                        senderroleindex = guildroles.index(i)
            for a in targetrole:
                if a == i:
                    if targetroleindex < guildroles.index(i):
                        targetroleindex = guildroles.index(i)

        if senderroleindex > targetroleindex:
            await ctx.send(f"Muted: {member.mention} for {length}seconds.")
            await member.add_roles(muterole)
            
            # Insert a row of data
            memberid = member.id
            membermention = member.mention
            discordid = ctx.guild.id
            unmutetime = datetime.now() + timedelta(seconds=length)
            active = "Active"
            con = sqlite3.connect('bot.db')
            cur = con.cursor()
            cur.execute("INSERT INTO moderation VALUES (?,?,?,?,?)", (discordid,memberid,membermention,unmutetime,active))
            con.commit()
            con.close()
        elif senderroleindex == targetroleindex or senderroleindex < targetroleindex:
            await ctx.send("Cannot mute someone with the same or greater role than you.")

    #@commands.command()
    #@commands.has_permissions(kick_members=True)
    #async def admintest(self, ctx):
       # await ctx.send("you can kick.")
    #@commands.command()
    #@commands.has_permissions(ban_members=True)
    #async def admintest2(self, ctx):
        #await ctx.send("you can Ban.")

    @commands.command()
    async def clear_messages(self, ctx, member: discord.Member, amount=10):
        await ctx.channel.purge(limit=amount, check=lambda m: m.author == member)
    
    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(title= '**Jackal**', url= 'https://discord.com/api/oauth2/authorize?client_id=889183519501328384&permissions=8&scope=bot')
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/ZzS0qALknuHHH2Jxb013cnQPqTLgYxh3YFDZ0gRZG7c/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/889183519501328384/b4b59d22618e50d0c4c620f61a8ff16c.png")
        embed.add_field(name='**Stats**', value= f'**Guilds** {len(self.client.guilds)}\n**Users** {len(self.client.users)}\n**Commands** {len(self.client.commands)}',inline=False)
        embed.add_field(name='**Infomation**', value= f'**Version** 1.0.0\n**DiscordPY** 1.7.3\n**Python** 3.8.2',inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Moderation(client))

    
