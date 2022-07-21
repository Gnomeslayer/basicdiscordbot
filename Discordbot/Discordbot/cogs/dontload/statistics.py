import discord, json, aiosqlite
from discord.ext import commands
 
class Statistics(commands.Cog):

    def __init__(self, client):
        print("[Cog] Statistics has been initiated")
        self.client = client
    
    @commands.command()
    async def comstats(self, ctx):
        async with aiosqlite.connect('bot.db') as db:
                #cur.execute('''CREATE TABLE IF NOT EXISTS statistics (guild_id, command_name, uses)''')
            guild_id = ctx.guild.id
            command_name = ''
            command_uses = ''
            commands_cursor = await db.execute("SELECT * FROM comstats WHERE guild_id = :guild_id", {"guild_id": guild_id})
            commands_rows = await commands_cursor.fetchall()
            for i in commands_rows:
                command_name += f"{i[1]}\n"
                command_uses += f"{i[2]}\n"
                
            embed = discord.Embed(title="Statistics for all commands.")    
            embed.add_field(name="Commands", value=command_name)
            embed.add_field(name="Uses", value=command_uses)
            await ctx.send(embed=embed)
            
    @commands.command()
    async def stats(self, ctx, member : discord.Member = None):
        if not member:
            member = ctx.author
        guild_id = ctx.guild.id
        member_id = member.id
        command_name = ''
        command_uses = ''
        async with aiosqlite.connect('bot.db') as db:
            commands_cursor = await db.execute("SELECT * FROM user_Stats WHERE guild_id = ? AND member_id = ?", (guild_id, member_id))
            commands_rows = await commands_cursor.fetchall()
            for i in commands_rows:
                command_name += f"{i[2]}\n"
                command_uses += f"{i[3]}\n"
        
        embed = discord.Embed(title=f"Command usages for {member.name}")
        embed.add_field(name="Commands", value=command_name)
        embed.add_field(name="Uses", value=command_uses)
        await ctx.send(embed=embed)
        
        
    @commands.Cog.listener()
    async def on_command_completion(self,ctx):
        async with aiosqlite.connect('bot.db') as db:
            guild_id = ctx.guild.id
            member_id = ctx.author.id
            command_name = ctx.command.name
            dbcount_users = await db.execute("SELECT COUNT(*) FROM user_stats WHERE guild_id = :guild_id AND member_id = :member_id AND command_name = :command_name", (guild_id, member_id, command_name))
            dbcount_commands = await db.execute("SELECT COUNT(*) FROM comstats WHERE guild_id = :guild_id AND command_name = :command_name", (guild_id, command_name))
            db_users_count = await dbcount_users.fetchall()
            db_commands_count = await dbcount_commands.fetchall()
            if db_users_count[0][0] == 0:
                await db.execute("INSERT INTO user_stats VALUES (?,?,?,?)", (guild_id,member_id,command_name,1))
            if db_users_count[0][0] == 1:
                task = (guild_id, member_id)
                await db.execute('UPDATE user_stats SET uses=uses + 1 WHERE guild_id=? AND member_id=?', task)
                
            if db_commands_count[0][0] == 0:
                await db.execute("INSERT INTO comstats VALUES (?,?,?)", (guild_id,command_name,1))
            if db_commands_count[0][0] == 1:
                task = (guild_id, command_name)
                await db.execute('UPDATE comstats SET uses=uses + 1 WHERE guild_id=? AND command_name=?', task)
            await db.commit()
            await dbcount_users.close()
            await dbcount_commands.close()

async def setup(client):
    await client.add_cog(Statistics(client))