
import os
import discord
import asyncio
import Bokai

from dotenv import load_dotenv
from discord.ext import commands as cmd

# Setting Up Logger
import logging
logging.basicConfig(level=logging.INFO)

load_dotenv()


# intents = discord.Intents.default()

cogs_list = ['cmds','todo','guessint','TicTacToeCog','misc','runpy']

# Initializing BOt
bot = discord.Bot(intents=discord.Intents.all())

# debug_guilds = Bokai.tools.get_guild()


@bot.event
async def on_ready():
    print("Logged in")
    # await asyncio.sleep(5)
    # user = bot.get_user(808587394915237918)
    # print(user)
    # await user.send("I'm online!")

# @bot.event
# async def on_message(message):
#     print(message.content)

# Loading Cogs

for cog in cogs_list:
    bot.load_extension(f'Bokai.cogs.{cog}')
    
# @bot.slash_command(guild_ids = [974922382110232586])
# async def hello(ctx):
#     await ctx.respond("Hello World!")

@bot.slash_command(guild_ids = [974922382110232586])
async def reload(ctx):
    for cog in cogs_list:
        
        bot.unload_extension(f'Bokai.cogs.{cog}')
        bot.load_extension(f'Bokai.cogs.{cog}')
        await ctx.respond(f"Reloaded {cog}")
    message = await ctx.send("Reloaded all modules")
    await message.add_reaction(emoji='✅')



@bot.slash_command(debug_guilds = Bokai.tools.get_guild(),description="Sends the bot's latency")
async def ping(ctx):
    embed=discord.Embed(title="🏓Pong!",description=f"Latency: {round(bot.latency * 1000)}ms",color=0x254bbb)
    embed.set_author(name="")
    await ctx.respond(embed=embed)


    




# Loading Token
try:
    bot.run(os.getenv('BOT_TOKEN'))
    # print(Bokai.tools.workingdir())
except Exception as exception:
    print("Failed to connect to Discord. Please check the bot token in .env")
    print(exception)