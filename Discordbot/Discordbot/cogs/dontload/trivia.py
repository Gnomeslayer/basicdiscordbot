from discord.ext import commands, tasks

 
class Trivia(commands.Cog):

    def __init__(self, client):
        print("[Cog] Trivia has been initiated")
        self.client = client
        
    @commands.command(help='[Starts a given task.]')
    @commands.is_owner()
    async def start_task(self,ctx, *, mytask):
        if mytask == 'TriviaA':
            await ctx.send("TriviaA starting..")
            self.TriviaA.start()

    @commands.command(help='[Stops a given task.]')
    @commands.is_owner()
    async def stop_task(self, ctx, *, mytask):
        if mytask == 'TriviaA':
            await ctx.send("TriviaA stopping..")
            self.TriviaA.stop()

    @tasks.loop(seconds=10)
    async def TriviaA(self):
        print("TriviaA")

def setup(client):
    client.add_cog(Trivia(client))
