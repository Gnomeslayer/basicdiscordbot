import discord,random,itertools,csv
from io import BytesIO
from discord.ext import commands

 
class FunFacts(commands.Cog):

    def __init__(self, client):
        print("[Cog] Fun facts has been initiated")
        self.client = client
        self.funfacts = []
        self.load_ff()
        self.iteration = itertools.cycle(self.funfacts)
        self.tts = False
        self.explicit_content = False
        self.random = True

    def load_ff(self):
        try:
            with open('funfacts.csv') as f:
                reader = csv.reader(f)
                datalist = list(reader)
                for a in datalist[0]:
                    self.funfacts.append(a)
                
        except:
            print("Failed to load fun facts from file. Probably doesn't exist. Created new file tho.")
            with open('funfacts.csv', 'w') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

    @commands.command()
    @commands.is_owner()
    async def save_ff(self,ctx):
        with open('funfacts.csv', 'w') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(self.funfacts)
            await ctx.send("Saved fun facts!")


    @commands.command(help='[Starts a given task.]',aliases=['ff'])
    async def funfact(self,ctx, command = None, number = None):
        print(f'{ctx.author} used {ctx.command.name}.')
        if len(self.funfacts) >= 1:
            if not command:
                if self.random == True:
                    random_number = random.randint(0, len(self.funfacts)-1)
                    await ctx.send(f"Fact {random_number}. {self.funfacts[random_number]}", tts=self.tts)
                else:
                    fact = next(self.iteration)
                    index = self.funfacts.index(fact)
                    await ctx.send(f"Face {index}. {fact}", tts=self.tts)
            else:
                if command == 'Random' or command == 'random' or command == 'rand' or command == 'r':
                    random_number = random.randint(0, len(self.funfacts)-1)
                    await ctx.send(f"Fact {random_number}. {self.funfacts[random_number]}", tts=self.tts)
                elif command == 'Specific' or command == 's':
                    if not number:
                        await ctx.send("You did not specify a number!", tts=self.tts)
                    else:
                        number = int(number)
                    if number < 0 or number >= len(self.funfacts):
                        await ctx.send(f"Your number was wrong. Enter a number between 0 and {len(self.funfacts)}", tts=self.tts)
                    else:
                        await ctx.send(f"Fact {number}. {self.funfacts[number]}", tts=self.tts)
                else:
                    fact = next(self.iteration)
                    index = self.funfacts.index(fact)
                    await ctx.send(f"Face {index}. {fact}", tts=self.tts)
        else:
            await ctx.send("There are no fun facts.", tts=self.tts)

    @commands.command(help='[Adds a fun fact!]', aliases=['ffa'])
    async def funfact_add(self,ctx, *, ff):
        print(f'{ctx.author} used {ctx.command.name}. They added this: {ff}')
        self.funfacts.append(ff)
        with open('funfacts.csv', 'w') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(self.funfacts)
            await ctx.send("Saved fun facts!")

    @commands.command(aliases=['ffr'])
    @commands.is_owner()
    async def funfact_remove(self, ctx, number:int):
        if number <= len(self.funfacts)-1 and number >= 0:
            self.funfacts.pop(number)
            with open('funfacts.csv', 'w') as myfile:
                wr = csv.writer(myfile)
                wr.writerow(self.funfacts)
                await ctx.send("Removed fun fact and saved list!")

    @commands.command(help='[Gives you a list of all the fun facts!]', aliases=['ffl'])
    @commands.is_owner()
    async def funfacts_list(self, ctx):
        if len(self.funfacts) >= 1:
            ff = ''
            counter = 0
            content = ''
            for i in self.funfacts:
                ff += (f'[{counter}] {i} \n')
                as_bytes = map(str.encode, ff)
                content = b''.join(as_bytes)
                counter += 1
            await ctx.send("Fun Facts List", file=discord.File(BytesIO(content), "fflist.txt"))
        else:
            await ctx.send("No fun facts to send.")

    @commands.command(help='[Settings for Fun Facts bot!]', aliases=['ffs', 'ffsettings'])
    @commands.is_owner()
    async def funfacts_settings(self, ctx, setting = None, update = None):
        if update == 'false':
            update = False
        if update == 'true':
            update = True

        if not setting and not update:
            embed = discord.Embed()
            embed.add_field(name="Settings", value=f"Text to speech: {self.tts}\nRandom: {self.random}", inline="False")
            await ctx.send(embed=embed)
        if setting == 'random':
            self.random = update
            await ctx.send("Updated the random setting.")
            embed = discord.Embed()
            embed.add_field(name="Settings", value=f"Text to speech: {self.tts}\nRandom: {self.random}", inline="False")
            await ctx.send(embed=embed)
        if setting == 'tts':
            self.tts = update
            await ctx.send("Updated the TTS setting.")
            embed = discord.Embed()
            embed.add_field(name="Settings", value=f"Text to speech: {self.tts}\nRandom: {self.random}", inline="False")
            await ctx.send(embed=embed)

        if setting == 'explicit_content' or setting == 'explicit':
            self.tts = update
            await ctx.send("Updated the explicit content setting.")
            embed = discord.Embed()
            embed.add_field(name="Settings", value=f"Text to speech: {self.tts}\nRandom: {self.random}", inline="False")
            await ctx.send(embed=embed)

        if setting == 'all':
            self.tts = update
            self.explicit_content = update
            await ctx.send("Updated all settings.")
            embed = discord.Embed()
            embed.add_field(name="Settings", value=f"Text to speech: {self.tts}\nRandom: {self.random}", inline="False")
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(FunFacts(client))
