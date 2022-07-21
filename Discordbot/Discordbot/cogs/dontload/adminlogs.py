import discord, sys, traceback
from discord.ext import commands
 
class Adminlogs(commands.Cog):

    def __init__(self, client):
        print("[Cog] Adminlogs has been initiated")
        self.client = client
        
        #Will display a notification if set to true.
        self.admin_command_completion = True
        self.admin_command_error = True
        self.admin_logs = True
        
        self.admin_message_delete = True
        self.admin_message_edit = True
        self.admin_message_react = True
        self.admin_message_bans = True
        
        self.admin_bans = True
        self.admin_member_join = True
        self.admin_member_remove = True
        self.admin_member_update = True
        
        self.admin_limit_discord = True
        self.discord = 794837147068792862
        
    @commands.Cog.listener()
    async def on_command_completion(self,ctx):
        commandname = str(ctx.command.name) #gets command name
        commandauthor = ctx.author #gets author of command
        userAvatar = commandauthor.avatar #gets the avatar of author

        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.

        #setups our command text to be potentially sent to the channel
        commandrun = f'{commandauthor} used the commaned: {commandname}.\n**This is what they typed**\n{ctx.message.content}'

        if self.admin_command_completion == True:
            embed = discord.Embed(title= '**Admin Logs**')
            embed.set_thumbnail(url=userAvatar)
            embed.add_field(name="Command Completed", value=commandrun)
            await channel.send(embed=embed)
            
            
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        commandname = str(ctx.command) #gets command name
        commandauthor = ctx.author #gets author of command
        userAvatar = commandauthor.avatar #gets the avatar of author

        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.

        #setups our command text to be potentially sent to the channel
        commandrun = f'{commandauthor} attempted to use the command: {commandname}'

        ignored = (commands.CommandNotFound, )

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            commandrun += '\nUnfortunately it was disabled.'
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                commandrun += '\nUnfortunately this command cannot be run in Private Messages.'
            except discord.HTTPException:
                pass #save this

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send('I could not find that member. Please try again.')
                commandrun += '\nUnfortunately the member in question could not be located.'
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('\n------------\nIgnoring exception in command\n------------\n {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            
            commandrun += '\nBut they typed the command wrong.'

        #if this function is enabled in the settings it will get displayed.
        if self.admin_command_error == True:
            if self.admin_limit_discord == True:
                if self.discord == ctx.guild.id:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.set_thumbnail(url=userAvatar)
                    embed.add_field(name="Command Completed", value=commandrun)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(title= '**Admin Logs**')
                embed.set_thumbnail(url=userAvatar)
                embed.add_field(name="Command Completed", value=commandrun)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.client.get_channel(889479625087021106)
        mydiscord = self.client.get_guild(message.guild.id)
        
        try:
            async for i in mydiscord.audit_logs(limit=1,action=discord.AuditLogAction.message_delete):
                deleter = i.user
        except:
            pass
        if (message.author.bot):
            return
        else:
            deletedmsg = f'Message Author: {message.author}\nMessage Content: {message.content}\nDeleter:{deleter}'
            if self.admin_message_delete == True:
                if self.admin_limit_discord == True:
                    if self.discord == message.guild.id:
                        embed = discord.Embed(title= '**Admin Logs**')
                        embed.add_field(name="Owner of the message", value=f'```{message.author}```', inline=True)
                        embed.add_field(name="Name of deleter", value=f'```{deleter}```', inline=True)
                        embed.add_field(name="Content", value=f'```{message.content}```', inline=False)
                        await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name="Owner of the message", value=f'```{message.author}```', inline=True)
                    embed.add_field(name="Name of deleter", value=f'```{deleter}```', inline=True)
                    embed.add_field(name="Content", value=f'```{message.content}```', inline=False)
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self,messages):
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        await channel.send(f"Bulk messages deleted.")
        mydiscord = self.client.get_guild(messages[0].guild.id)
        msg = ''
        try:
            async for i in mydiscord.audit_logs(limit=1,action=discord.AuditLogAction.message_delete):
                deleter = i.user
        except:
            pass
        msg += f'{deleter} deleted {len(messages)} message(s).\n'
        if len(messages) > 5:
            msg += '**Only displaying 5 messages**\n'
        a = 0
        for i in messages:
            if a == 5:
                break
            msgauthor = i.author
            msgcontent = i.content
            msg += f'**Message Author**: {msgauthor}\n{msgcontent}\n'
            a += 1
            
        if self.admin_message_delete == True:
            if self.admin_limit_discord == True:
                if self.discord == messages[0].guild.id:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name="Bulk messages deleted", value=f'{msg}', inline=False)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name="Bulk messages deleted", value=f'{msg}', inline=False)
                await channel.send(embed=embed)
                        
                        

    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        oldmessage = before.content
        newmessage = after.content
        author = before.author
        if self.admin_message_edit == True:
            if self.admin_limit_discord == True:
                if self.discord == before.guild.id:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name=f"Message has been edited.", value=f'{author} edited their message', inline=False)
                    embed.add_field(name=f"Original message", value=f'```{oldmessage}```', inline=False)
                    embed.add_field(name=f"New message", value=f'```{newmessage}```', inline=False)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name=f"Message has been edited.", value=f'{author} edited their message', inline=False)
                embed.add_field(name=f"Original message", value=f'```{oldmessage}```', inline=False)
                embed.add_field(name=f"New message", value=f'```{newmessage}```', inline=False)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        reactedmessage = reaction.message.content
        reactedmessageauthor = reaction.message.author
        reactionemoji = reaction.emoji
        msg = f'**Message Author**: {reactedmessageauthor}\n```{reactedmessage}```'
        if self.admin_message_react == True:
            if self.admin_limit_discord == True:
                if self.discord == user.guild.id:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name=f"A message has been reacted to.", value=f'{user} reacted to a message', inline=False)
                    embed.add_field(name=f"Message they reacted to", value=msg, inline=False)
                    embed.add_field(name=f"Reaction", value=f'```{reactionemoji}```', inline=False)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name=f"A message has been reacted to.", value=f'{user} reacted to a message', inline=False)
                embed.add_field(name=f"Message they reacted to", value=msg, inline=False)
                embed.add_field(name=f"Reaction", value=f'```{reactionemoji}```', inline=False)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self,reaction, user):
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        reactedmessage = reaction.message.content
        reactedmessageauthor = reaction.message.author
        reactionemoji = reaction.emoji
        msg = f'**Message Author**: {reactedmessageauthor}\n```{reactedmessage}```'
        if self.admin_message_react == True:
            if self.admin_limit_discord == True:
                if user.guild.id == self.discord:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name=f"Reaction removed.", value=f'{user} removed a reaction.', inline=False)
                    embed.add_field(name=f"Message they removed reaction from", value=msg, inline=False)
                    embed.add_field(name=f"Reaction removed", value=f'```{reactionemoji}```', inline=False)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name=f"Reaction removed.", value=f'{user} removed a reaction.', inline=False)
                embed.add_field(name=f"Message they removed reaction from", value=msg, inline=False)
                embed.add_field(name=f"Reaction removed", value=f'```{reactionemoji}```', inline=False)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_clear(self,message, reactions):
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        reactedmessage = message.content
        reactedmessageauthor = message.author
        reactionemoji = ''
        for reaction in reactions:
            reactionemoji += reaction.emoji
            
        msg = f'**Message Author**: {reactedmessageauthor}\n```{reactedmessage}```'
        if self.admin_message_react == True:
            if self.admin_limit_discord == True:
                if message.guild.id == self.discord:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name=f"Reactions cleared.", value=f'Reactions have been cleared from a comment.', inline=False)
                    embed.add_field(name=f"Message with reactions", value=msg, inline=False)
                    embed.add_field(name=f"Reaction removed", value=f'```{reactionemoji}```', inline=False)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name=f"Reactions cleared.", value=f'Reactions have been cleared from a comment.', inline=False)
                embed.add_field(name=f"Message with reactions", value=msg, inline=False)
                embed.add_field(name=f"Reaction removed", value=f'```{reactionemoji}```', inline=False)
                await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_unban(self,guild,user):
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        bannedfrom = guild.name
        banneduser = user.name
        msg = f'**Guild**\n{bannedfrom}\n**Member unbanned**\n{banneduser}'
        if self.admin_bans == True:
            if self.admin_limit_discord == True:
                if self.discord == guild.id:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name=f"User has been unbanned", value=f'{msg}', inline=False)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name=f"User has been unbanned", value=f'{msg}', inline=False)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self,guild, user):
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        bannedfrom = guild.name
        banneduser = user.name
        msg = f'**Guild**\n{bannedfrom}\n**Member banned**\n{banneduser}'
        if self.admin_bans == True:
            if self.admin_limit_discord == True:
                if self.discord == guild.id:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name=f"User has been banned", value=f'{msg}', inline=False)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name=f"User has been banned", value=f'{msg}', inline=False)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        title = 'A user updated themselves!'
        msg = 'Something undedected was picked up.'
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        if before.avatar.url != after.avatar.url:
            title = f'{after} changed their avatar!'
            msg = f'Old avatar: {before.avatar}\nNew avatar: {after.avatar}'
        if before.discriminator != after.discriminator:
            title = f'Discriminator change for {after}'
            msg = f'Old discriminator: {before.discriminator}\nNew discriminator: {after.discriminator}'
        if self.admin_member_update == True:
            if self.admin_limit_discord == True:
                if self.discord == before.guild.id:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name=title, value=f'```{msg}```', inline=False)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name=title, value=f'```{msg}```', inline=False)
                await channel.send(embed=embed)
                     
    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        title = 'A user updated their presence!'
        msg = f'{before.display_name} has updated their presence.'
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        if before.status != after.status:
            title = f'Status change for {after}'
            msg = f'Old status: {before.status}\nNew status: {after.status}'
        if before.activity != after.activity:
            title = f'Activity change for {after}'
            msg = f'Old activity: {before.activity}\nNew Activity: {after.activity}'
        
        if self.admin_member_update == True:
            if self.admin_limit_discord == True:
                if self.discord == before.guild.id:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name=title, value=f'```{msg}```', inline=False)
                    await channel.send(embed=embed)
            else:
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name=title, value=f'```{msg}```', inline=False)
                await channel.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        title = 'A member updated themselves!'
        msg = 'Something went unnoticed.'
        
        if before.display_name != after.display_name:
            title = f'Display name change of {after}'
            msg = f'Old display name: {before.display_name}\nNew display name: {after.display_name}'
            if self.admin_member_update == True:
                if self.admin_limit_discord == True:
                    if self.discord == before.guild.id:
                        embed = discord.Embed(title= '**Admin Logs**')
                        embed.add_field(name=title, value=f'```{msg}```', inline=False)
                        await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name=title, value=f'```{msg}```', inline=False)
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        if self.admin_member_join == True:
            if self.admin_limit_discord == True:
                if self.discord == member.guild.id:
                    msg = f'{member.name} has joined Guild.'
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name="Member joined", value=f'```{msg}```', inline=False)
                    await channel.send(embed=embed)
            else:
                msg = f'{member.name} has joined Guild.'
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name="Member joined", value=f'```{msg}```', inline=False)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(889479625087021106) #Channel where this log will be sent.
        if self.admin_member_remove == True:
            if self.admin_limit_discord == True:
                if self.discord == member.guild.id:
                    msg = f'{member.name} has left the guild.'
                    embed = discord.Embed(title= '**Admin Logs**')
                    embed.add_field(name="Member removed", value=f'```{msg}```', inline=False)
                    await channel.send(embed=embed)
            else:
                msg = f'{member.name} has left the guild.'
                embed = discord.Embed(title= '**Admin Logs**')
                embed.add_field(name="Member removed", value=f'```{msg}```', inline=False)
                await channel.send(embed=embed)


def setup(client):
    client.add_cog(Adminlogs(client))