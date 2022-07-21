import discord, sqlite3, json, asyncio, time, os
from discord.ext import commands
import discord.utils

''' 
You will need a new bot token, so follow this quick guide on how to create a bot:
https://discordpy.readthedocs.io/en/latest/discord.html
'''
bottoken = 'Discord bot token.'

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

#Sends messages whenever a user joins, leaves or is removed.
@bot.event
async def on_ready():
    print('Bot is ready')
    #print(bot.guilds)
#Sends messages whenever a user joins, leaves or is removed.


#@bot.event
#async def on_message(message):
#    if message.author != bot.user:
#        if message.content.lower().isdigit():
#            mynumber = int(message.content)
#            mynumber += 1
#            await message.channel.send(mynumber)
#    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    pass

def dbsetup():
    con = sqlite3.connect('bot.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS moderation
        (discordid,userid,usermention,unbantime,active)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS reminder
        (discordid,memberid,membermention,remindtime,message,active)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS invites (guild_id, member_id, invites, PRIMARY KEY (member_id))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS comstats (guild_id, command_name, uses)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS user_stats (guild_id, member_id, command_name, uses)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS funfacts (guild_id, member_id, funfact, funfact_descrption, nsfw, category)''')

    con.commit()
    con.close()
    print("Database ready.")
    
    
#Loads the cogs
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    #channel = bot.get_channel(889479625087021106)
    await bot.load_extension(f'cogs.{extension}')
    await ctx.channel.send(f"Loaded {extension}")

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    #channel = bot.get_channel(889479625087021106)
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.channel.send(f"Unloaded {extension}")

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    #channel = bot.get_channel(889479625087021106)
    extension = extension.lower()
    await bot.unload_extension(f'cogs.{extension}')
    await asyncio.sleep(1)
    await bot.load_extension(f'cogs.{extension}')
    await ctx.channel.send(f'Reloaded {extension}')

@bot.command()
@commands.is_owner()
async def showdiscords(ctx):
    print(bot.guilds)
    await ctx.send(bot.guilds)
    

dbsetup()
time.sleep(1)
async def setup():
    # Location of the COG files.
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            if "bm" not in filename:
                await bot.load_extension(f"cogs.{filename[:-3]}")

    await bot.start(bottoken)


asyncio.run(setup())