import asyncpraw, discord, datetime
from datetime import datetime
from discord.ext import commands, tasks
import json

class Reddit(commands.Cog):
    
    
    def __init__(self, client):
        print("[Cog] Reddit has been initiated")
        self.client = client
        #Login details. You will need to get your api connection keys from reddit.
        self.reddit = asyncpraw.Reddit(
            client_id="reddit client id",
            client_secret="reddit client secret",
            password="reddit password",
            user_agent="Discordbot by u/haroerhaktak", #this can be whatever
            username="reddit username"
        )
    
    #starts the auto feature.
    @commands.command()
    @commands.is_owner() #Limits it to just the owner of the bot. However you can change to has_role or has_roles or even permissions.
    async def startunread(self, ctx):
        await ctx.send("Starting the auto unread feature.")
        self.autounread.start(ctx.author)
    
    #stops the auto feature.
    @commands.command()
    @commands.is_owner() #Limits it to just the owner of the bot. However you can change to has_role or has_roles or even permissions.
    async def stopunread(self, ctx):
        await ctx.send("Stopping the auto unread feature.")
        self.autounread.stop()
        
    #The auto feature checks every 60 seconds. I feel 60 seconds is a good time to update. But you can change to whatever you feel necessary.
    @tasks.loop(seconds=60)
    async def autounread(self, member: discord.Member):
        print(f"60 seconds has passed. Still running.{datetime.now()}") #Gives me peace of mind knowing it's still running and not bugged out.
        mention = member.mention
        guild = member.guild
        
        inbox = self.reddit.inbox.unread()
        unreadmessages = []
        async for message in inbox:
            content = {
                'id': message.id,
                'name': message.name,
                'message': message.body,
                'author': message.author
            }
            unreadmessages.append(content)
        #The channel you want to create the threads on.
        #Anybody who can see/access the channel can see public_threads, so be careful.
        channel = self.client.get_channel(996684990362427502)
        if len(unreadmessages) == 0:
            nounread = await channel.send("No unread messages to show you.")
            await nounread.delete(delay=30)
        else:
            #Grab the data of the comment and where it came from.
            for i in unreadmessages:
                create_thread_bool = True
                for thread in guild.threads:
                    if str(thread) == str(i['id']):
                        create_thread_bool = False
                if create_thread_bool == True:
                    thecomment = await self.reddit.comment(id=i['id'])
                    parent = await thecomment.parent()
                    if parent._kind == 't3':
                        continue
                    
                    postcomment = "post"
                    if hasattr(parent, 'body'):
                        parent = parent.body
                        postcomment = "Comment"
                    if hasattr(parent, 'id'):
                        newcomment = await self.reddit.comment(id=parent.id)
                        parent = newcomment.body
                    #Spit it out in a nice format that's easy to read and understand.
                    subreddit = thecomment.subreddit
                    create_thread = await channel.send("Creating a new thread for an unread message.")
                    thread = await channel.create_thread(name=f'{i["id"]}', message=create_thread)
                    embed = discord.Embed(title= '**Reddit Inbox**', description=f'{i["message"]}')
                    embed.add_field(name="Message from", value=f'```{i["author"]}```', inline=True)
                    embed.add_field(name="Message subreddit", value=f'```{subreddit}```', inline=True)
                    embed.add_field(name=f"Reply was to this {postcomment}", value=f'```{parent}```', inline=False)
                    await thread.send(f"Welcome to this unread message {mention}.\nTo reply type $reply <message>\nTo mark as read type $markread\nTo simply close this thread, type $close (will not mark as read)")
                    await thread.send(embed=embed)
                    await create_thread.delete(delay=2)
        unreadmessages = []
    
    #Does the same as autounread except only runs once.      
    @commands.command()
    @commands.is_owner()
    async def unread(self, ctx):
        inbox = self.reddit.inbox.unread()
        guild = ctx.guild
        mention = ctx.author.mention
        unreadmessages = []
        async for message in inbox:
            content = {
                'id': message.id,
                'name': message.name,
                'message': message.body,
                'author': message.author
            }
            unreadmessages.append(content)
        channel = self.client.get_channel(996684990362427502)
        if len(unreadmessages) == 0:
            nounread = await channel.send("No unread messages to show you.")
            await nounread.delete(delay=30)
        else:
            for i in unreadmessages:
                #Check to ensure the message hasn't already been opened. We don't want duplicates.
                create_thread_bool = True
                for thread in guild.threads:
                    if str(thread) == str(i['id']):
                        create_thread_bool = False
                if create_thread_bool == True:
                    thecomment = await self.reddit.comment(id=i['id'])
                    parent = await thecomment.parent()
                    postcomment = "post"
                    try:
                        try:
                            parent = parent.body
                            postcomment = "comment"
                        except:
                            parent = parent.title
                    except:
                            newcomment = await self.reddit.comment(id=parent.id)
                            parent = newcomment.body
                    
                    subreddit = thecomment.subreddit
                    create_thread = await channel.send("Creating a new thread for an unread message.")
                    thread = await channel.create_thread(name=f'{i["id"]}', message=create_thread)
                    embed = discord.Embed(title= '**Reddit Inbox**', description=f'{i["message"]}')
                    embed.add_field(name="Message from", value=f'```{i["author"]}```', inline=True)
                    embed.add_field(name="Message subreddit", value=f'```{subreddit}```', inline=True)
                    embed.add_field(name=f"Reply was to this {postcomment}", value=f'```{parent}```', inline=False)
                    await thread.send(f"Welcome to this unread message {mention}.\nTo reply type $reply <message>\nTo mark as read type $markread\nTo simply close this thread, type $close (will not mark as read)")
                    await thread.send(embed=embed)
                    await create_thread.delete(delay=2)
        unreadmessages = []
    
    #Marks a "comment" as read.   
    @commands.command()
    @commands.is_owner()
    async def markread(self, ctx):
        if str(ctx.channel.type) == 'public_thread':
            comment = await self.reddit.comment(str(ctx.channel.name))
            await comment.mark_read()
            await ctx.channel.delete()
    
    #Replys to a comment and then marks it as read. There's no reason to keep it around.      
    @commands.command()
    @commands.is_owner()
    async def reply(self, ctx, *, reply):
        if str(ctx.channel.type) == 'public_thread':
            comment = await self.reddit.comment(str(ctx.channel.name))
            replymsg = reply
            await comment.reply(replymsg)
            await comment.mark_read()
            await ctx.channel.delete()
    
    #Closes the thread without doing anything to the comment. Because why do something now when we can do it later?       
    @commands.command()
    @commands.is_owner()
    async def close(self, ctx):
        if str(ctx.channel.type) == 'public_thread':
            await ctx.channel.delete()
            
async def setup(client):
    await client.add_cog(Reddit(client))
