import discord
from discord.ext import commands
import subprocess
import sys
from  Bokai.utils.Modals import Modal_Input_of_Runpy

class runpy(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.slash_command()
    async def python3(self,ctx):
        modal = Modal_Input_of_Runpy(title = "Run your python3 Code")
        await ctx.send_modal(modal)




def setup(bot):
    bot.add_cog(runpy(bot))