import discord
from discord.ext import commands
import Bokai



class cmds(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot



    

    

    @discord.slash_command()
    async def greet(self, ctx, member: discord.Member):
        message = await ctx.respond(f'{ctx.author.mention} says hello to {member.mention}!')
        print(message)

    @discord.slash_command(debug_guilds = Bokai.tools.get_guild())
    async def purge(self,ctx, amount:discord.Option(int)):
        if amount > 50:
            await ctx.respond('You can only delete 50 messages at a time.')
            return
        await ctx.channel.purge(limit=amount)
        await ctx.respond(f'{ctx.author.mention} has purged {amount} messages!')

    

    @commands.Cog.listener() # we can add event listeners to our cog
    async def on_member_join(self, member): # this is called when a member joins the server

        await member.send('Welcome to the server!')
    
    



def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(cmds(bot))