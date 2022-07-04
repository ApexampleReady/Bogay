import discord
from discord.ext import commands
import subprocess
import sys


class Modals(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


class Modal_Input_of_Runpy(discord.ui.Modal):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.add_item(discord.ui.InputText(label="Your Python Code",placeholder="Example: print('Hello World')",style=discord.InputTextStyle.long))
    

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        username = member.name + '#' + member.discriminator
        print(username)
        embed = discord.Embed(title="Code Results")

        try:
            yourcode = self.children[0].value
        except:
            yourcode = "print('Hello World')"
        if yourcode == "":
            yourcode = "print('Hello World')"
        try:
            run = subprocess.run(
                [sys.executable, "-c", yourcode], capture_output=True, text=True
            )
            print(run.stdout,run.stderr)
            print(type(run.stderr))
            if run.stdout == None or run.stdout == '':
                embed.add_field(name="Output", value="No output")
            else:
                embed.add_field(name="Output", value=run.stdout)
            if run.stderr != "":
                embed.add_field(name="Error:", value=run.stderr, inline=False)
            # else:
            #     embed.add_field(name="Output:", value=run.stdout, inline=False)
                
                # await interaction.response.send_message(f"Output : \n{run.stdout} \n\n Error : \n {run.stderr}")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Exception Occurd : {e}")






def setup(bot):
    bot.add_cog(Modals(bot))