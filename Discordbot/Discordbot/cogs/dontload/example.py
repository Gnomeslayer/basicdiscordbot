import discord, random, asyncio, re
from urllib import parse, request
from discord.ext import commands

from discord.ext.commands import bot

 
class Example(commands.Cog):
    
    def __init__(self, client):
        print("[Cog] Example has been initiated")
        self.client = client

    @commands.command(help='[8 Ball.]',aliases=['8ball'])
    @commands.is_owner()
    async def _8ball(self,ctx, *, question = ''):
        if question == '':
            await ctx.send("Please enter a question.")
        else:
            responses = ['It is certain.',
                         'It is decidedly so.',
                         'Without a doubt',
                         'Yes - Definitely,',
                         'You may rely on it.',
                         'Most Likely.',
                         'Outlook good',
                         'Yes.',
                         'Signs point to yes',
                         'Reply hazy, try again',
                         'Better not tell you now',
                         'Cannot predict now.',
                         'Concentrate and ask again.',
                         'Dont count on it',
                         'My reply is no.',
                         'My sources say no.',
                         'Outlook not so god.',
                         'Very doubtful']
            await ctx.send(f'Question: {question}\nAnswer:{random.choice(responses)}')

    @commands.command(help='[Messages the targeted channel.]')
    @commands.is_owner()
    async def msgchan(self,ctx, chanid):
        channel = bot.get_channel(int(chanid))
        await channel.send('Hello')

    @commands.command(help='[Creates an invite link]')
    @commands.is_owner()
    async def createinvite(self,ctx):
        uses = 0
        time_in_seconds = 0
        invitelink = await discord.abc.GuildChannel.create_invite(ctx.message.channel,max_uses=0,max_age=0)
        await ctx.send(invitelink)

    @commands.command(help='[Sends an embed image]')
    @commands.is_owner()
    async def sendimage(self,ctx):
    # Rewrite
        file = discord.File("C:/Users/Declan/Desktop/discordbot/Discordbot/Discordbot/cow.png", filename="fish.png") # an image in the same folder as the main bot file
        embed = discord.Embed() # any kwargs you want here
        embed.add_field(name="Fiverr Header", value="Hello Fiverr", inline="False")
        embed.set_image(url="attachment://fish.png")
        embed.set_thumbnail(url="attachment://fish.png")
        embed.add_field(name="Fiverr Body", value="This could be yours!", inline="False")
        # filename and extension have to match (ex. "thisname.jpg" has to be "attachment://thisname.jpg")
        await ctx.send(embed=embed,file=file)

    @commands.command(help='[Sends the avatar of the mentioned user.]')
    @commands.is_owner()
    async def avatar(self, ctx, *, member: discord.Member):
        userAvatar = member.avatar_url

        embed = discord.Embed(color = member.color, timestamp = ctx.message.created_at)
        embed.set_author(name = f'Avatar of {member}')
        embed.set_image(url = userAvatar)
        embed.set_footer(text = f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def dothing(self, ctx):
        file = discord.File("C:/Users/Declan/Desktop/discordbot/Discordbot/Discordbot/cow.png", filename="fish.png") # an image in the same folder as the main bot file
        #file2 = discord.File("C:/Users/Declan/Desktop/example2.png", filename="fish.png") # an image in the same folder as the main bot file
        embed = discord.Embed() # any kwargs you want here
        embed.add_field(name="Fiverr Header", value="Hello Fiverr", inline="False")
        embed.set_image(url="attachment://fish.png")
        embed.set_thumbnail(url="attachment://fish.png")
        embed.add_field(name="Fiverr Body", value="This could be yours!", inline="False")
        # filename and extension have to match (ex. "thisname.jpg" has to be "attachment://thisname.jpg")
        await ctx.send(embed=embed,file=file)
        asyncio.sleep(2)
        file = discord.File('C:/Users/Declan/Desktop/discordbot/Discordbot/Discordbot/example2.png', filename="fish2.png")
        embed.set_image(url="attachment://fish2.png")
        await ctx.send(embed=embed,file=file)

    @commands.command(help='[Pew Pew.]')
    @commands.is_owner()
    async def kill(self,ctx, member : discord.Member):
        if ctx.author.mention == member.mention:
            await ctx.send(f'{ctx.author.mention} has just killed himself.. for the 16th time..')
        else:
            await ctx.send(f'{ctx.author.mention} has killed {member.mention}. <Sigh> _Not again._')
    

    @commands.command()
    @commands.is_owner()
    async def banuser(self, ctx, member : discord.Member, *, reason=None):
        for check in ctx.guild.members:
            if check.mention == member.mention:
                #Ban stuff here.
                pass
            else:
                #couldnt find him sir.
                pass

    @commands.command()
    @commands.is_owner()
    async def myroles(self, ctx):
        await ctx.send(ctx.guild.roles)
        await ctx.send(discord.utils.get(ctx.guild.roles))

    @commands.command()
    async def youtube(self, ctx, *, search):
        query_string = parse.urlencode({'search_query': search})
        html_content = request.urlopen(f'https://www.youtube.com/results?search_query={search}')
        print(html_content)

        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', html_content.read().decode())
        print(search_results)

    @commands.command(aliases=["SERVERINFO", "Serverinfo", "Serverinformation", "SERVERINFORMATION", "serverinformation"])
    async def serverinfo(self,ctx):
        embed = discord.Embed()
        fields = [("ID", ctx.guild.id, True),
                  ("Owner", ctx.guild.owner, True),
                  ("Region", ctx.guild.region, True),
                  ("Created at", ctx.guild.created_at.strftime("%m/%d/%Y %H:%M:%S"), True),
                  ("Members", len(ctx.guild.members), True),
                  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("Text channels", len(ctx.guild.text_channels), True),
                  ("Voice channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("\u200b", "\u200b", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        print(type(embed))
        print(embed.fields[0])
        await ctx.send(embed.fields)
        await ctx.send(embed=embed)

    @commands.command()
    async def search_for_channel_and_category(self, ctx):
        all_channels = []
        all_categories = []
        for category in ctx.guild.categories:
            all_categories.append(category)
        for channel in ctx.guild.text_channels:
                all_channels.append(channel)
             
        category_exists = False
        channel_exists = False
        for i in all_channels:
            if i.name == 'mailer-logs':
                channel_exists = True
        for i in all_categories:
            if i.name == 'mailer':
                category_exists = True

        if category_exists == True and channel_exists == True:
            print("Category and channel exists")
        elif category_exists == True and channel_exists == False:
            print("Category exists but channel does not")
        elif category_exists == False and channel_exists == True:
            print("Category doesn't exist but channel does exist")
        else:
            print("Nothing exists. We're doomed.")

    @commands.command()
    async def vcchess(self, ctx):
        authorids = [827123687055949824,853535211581341737,738609666505834517,
                    826823454081941545,886120777630486538,799975931224784897,
                    853306806116548609,757832621769097226, 197979859773947906]
        if ctx.author.id in authorids:
            #await ctx.message.delete()
            authorchannelid = ctx.author.voice.channel.id
            await ctx.send(authorchannelid)
            #link = await togetherControl.create_link(authorchannelid, 'chess')
            #print(link)
            
    @commands.command()
    async def ci(self,ctx):
        if ctx.author.guild_permissions.create_instant_invite == True and discord.ext.commands.bot_has_permissions(create_instant_invite = True):
            invites = await ctx.channel.create_invite()
            embed = discord.Embed(
                title = ':heavy_check_mark: Action Completed',
                description = f'Here is your invite: {invites}',
                colour = discord.Colour.green()
            )
            embed.set_footer(text='Enjoy!')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title = ':x: Action Failed',
                description = 'It is because you or the bot do not have the permission `create_instant_invite`.',
                colour = discord.Colour.red()
            )
            embed.set_footer(text='Please double-check again.')
            await ctx.send(embed=embed)
            
def setup(client):
    client.add_cog(Example(client))