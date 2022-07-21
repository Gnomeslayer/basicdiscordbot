import asyncpraw, discord, datetime
from datetime import datetime
from discord.ext import commands, tasks
import json

class Emojis(commands.Cog):
    
    
    def __init__(self, client):
        print("[Cog] Emojis has been initiated")
        self.client = client
    
    @commands.command()
    async def emojis(self, ctx):
        emoji_names = ''
        for emoji in ctx.guild.emojis:
            emoji_names += f'[{emoji.name} <:{emoji.name}:{emoji.id}>]'
        await ctx.send(f'{emoji_names}')
            
async def setup(client):
    await client.add_cog(Emojis(client))
