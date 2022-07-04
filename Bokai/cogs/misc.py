import discord
import Bokai
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
import qrcode
import os
from Bokai.utils.buttons import NitroView
from Bokai.utils.buttons import Google
import akinator as ak
import asyncio
import requests
from bs4 import BeautifulSoup
import json



# class Nitro_Button(discord.ui.View):
#     @discord.ui.button(label = "Claim Nitro", style = discord.ButtonStyle.green, emoji="💎")
#     async def button_callback(self,button,interaction):



class misc(commands.Cog,name="Misc",description = "All Miscellaneous commands are in here!"):

    def __init__(self,bot):
        self.bot = bot
    

    

    

    @discord.slash_command(description="Generate a Qrcode!")
    async def qrcode(self, ctx, url: Option(str, "The link you want the qrcode of", required=True, default=None), hidden: Option(str, "Do you want the qrcode to be visible only to you?", choices=["Yes", "No"], required=False, default=None)):
        img = qrcode.make(url)
        img.save("qrcode.png")
        if hidden == "Yes":
            await ctx.respond(content="**Here is your QRCode**", file=discord.File("qrcode.png"), ephemeral=True)
        else:
            await ctx.respond(content="**Here is your QRCode**", file=discord.File("qrcode.png"))
        os.remove("qrcode.png")
# file = discord.File(Bokai.tools.workingdir('images/nitro.png'))


    @discord.slash_command(description="Get a nice cat image!")
    async def cat(self, ctx):
        """ Get a cat image """
        req = requests.get('https://api.thecatapi.com/v1/images/search')
        if req.status_code != 200:
            await ctx.message.add_reaction(emoji='❌')
            await ctx.respond("API error, could not get a meow")
            print("Could not get a meow")
        catlink = json.loads(req.text)[0]
        rngcat = catlink["url"]
        em = discord.Embed()
        em.set_image(url=rngcat)
        await ctx.respond(embed=em)

    

    @discord.slash_command(description="Generates a nitro link!")
    async def nitro(self, ctx):
        interaction: discord.Inteaction = ctx.interaction
        embed = discord.Embed(description=f"**{ctx.author.mention} generated a nitro link!**", color=discord.Color.nitro_pink())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_message()
        await message.edit(embed=embed, view=NitroView(message, ctx))


    @discord.slash_command(description="Google Search")
    async def google(self,ctx,*,
                query: Option(str, "Type what you want to search!", required=True, default=None)):
        await ctx.respond(f"Google Result for {query}",view = Google(query))
    



    @discord.slash_command(description="Play a game of akinator")
    async def akinator(self, ctx: commands.Context):
        """Play a game of akinator\nHow to play: Think of a character it can either be a fictional or non-fictional character.\nThe bot will ask questions, just give them the right answer!"""
        await ctx.send(embed=discord.Embed(description="**Akinator is here to guess!\n--------------------------------\nOptions: y: `yes\n`no: `n`\nidk: `Don't know`\np: `probably`\npn: `probably not`\nb: `previous question`\nq: `quit the game`**", color=discord.Color.green()).set_image(url="https://static.wikia.nocookie.net/video-game-character-database/images/9/9f/Akinator.png/revision/latest?cb=20200817020737"))
        def check(msg):
            return (
                msg.author == ctx.author
                and msg.channel == ctx.channel
                and msg.content.lower() in ["y", "n", "idk", "p", "pn", "b", "q"]
            )

        try:
            aki = ak.Akinator()
            q = aki.start_game()
            while aki.progression <= 80:
                await ctx.send(embed=discord.Embed(description=f"**{q}\n\n[`y` | `n` | `idk` | `p` | `pn` | `b` | `q`]**", color=discord.Color.embed_background(theme="dark")))
                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=60)
                    if msg.content.lower() == "q":
                        await ctx.send(embed=discord.Embed(description="**You have quit the game!**", color=discord.Color.red()))
                        break
                    if msg.content.lower() == "b":
                        try:
                            q = aki.back()
                        except ak.CantGoBackAnyFurther:
                            await ctx.send(embed=discord.Embed(description=f"**<:error:897382665781669908> {e}**"))
                            continue
                    else:
                        try:
                            q = aki.answer(msg.content.lower())
                        except ak.InvalidAnswerError as e:
                            await ctx.send(embed=discord.Embed(description=f"**<:error:897382665781669908> {e}**"))
                            continue
                except asyncio.TimeoutError:
                    return await ctx.send(embed=discord.Embed(description=f"**<:error:897382665781669908> The game timed-out.. try plsying a new one**"))

                except Exception as e:
                    await ctx.send(embed=discord.Embed(description=f"**<:error:897382665781669908> An error occured\n`{str(e).capitalize()}`**"))
            aki.win()
            await ctx.send(
                embed=discord.Embed(description=f"**Is it {aki.first_guess['name']}\n({aki.first_guess['description']})!\nWas I correct?(y/n)\n\t**", color=discord.Color.orange()).set_image(url=aki.first_guess['absolute_picture_path'])
            )
            correct = await self.bot.wait_for("message", check=check)
            if correct.content.lower() == "y":
                await ctx.send(embed=discord.Embed(description="**Yay!**", color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(description="**Oof!**", color=discord.Color.red()))
        except Exception as e:
            await ctx.send(e)

    



def setup(bot):
    bot.add_cog(misc(bot))