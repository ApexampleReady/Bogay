from logging import exception


from unittest.util import sorted_list_difference
import Bokai
import discord
from discord.ext import commands
import time
import random

rank_database = {}

class guessint(commands.Cog):


    def __init__(self,bot):
        self.bot = bot
    
    guess = discord.SlashCommandGroup("guessint","Commands of the guessint module")

    @guess.command(description="Shows all the guessint commands in the guessint module")
    async def help(self,ctx: discord.ApplicationContext):
        embed=discord.Embed(title="*Guessint Commands*")
        embed.add_field(name="/guess start", value="Starts a new game", inline=True)
        # embed.add_field(name="/guess [number]", value="Guesses a number", inline=True)
        embed.add_field(name="/guess end", value="Ends the game", inline=True)
        await ctx.respond(embed=embed)
        msg = await self.bot.wait_for('message')
        await ctx.send("detected message")
    
    @guess.command(description="Starts a new game")
    async def start(self,ctx: discord.ApplicationContext):

        member = ctx.author.name + '#' + ctx.author.discriminator
        number = []
        number = Bokai.tools.random_number()
        print(number)
        await ctx.respond("Start Guessing :D")
        count = 0
        while True:
            msg = await self.bot.wait_for('message')
            
            
            user_input = list(msg.content)
            
            # print(msg)
            print(user_input)

            if ctx.author == msg.author:

                if msg.content.isdigit():
                    
                    if list(user_input) == number:
                        count += 1
                        await ctx.respond(f"You guessed it in {count} tries")
                        if member in rank_database and count < rank_database[member]:
                            rank_database[member] = count
                        elif member not in rank_database:
                            rank_database[member] = count
                        
                        break
                    elif len(user_input) != 4:
                        await ctx.respond("This number should be a 4 digit number")
                        continue
                        # if len(str(user_input)) < len(str(number)):
                        #     user_input = ('0' * (len(str(number)) - len(str(user_input)))) + str(user_input)
                        # elif len(str(user_input)) > len(str(number)):
                        #     number = ('0' * (len(str(user_input)) - len(str(number)))) + str(number)
                        

                        # for i in range(len(number)):
                        #     if(number[i] == user_input[i] and number[i] != '0'):
                        #         A_count += 1
                        # for i in range(len(number)):
                        #     for j in range(i+1,len(number)):
                        #         if(number[i] == user_input[j]):
                        #             B_count += 1
                    else:
                        result = 0
                        for i in range(0,len(number)):
                            for j in range(0,len(number)):
                                if user_input[i] == number[j]:
                                    if i == j:
                                        result += 10
                                    else:
                                        result += 1
                        count += 1
                        # if result == 40:
                        #     await ctx.respond(f"You guessed it in {count} tries!")
                        #     break
                        # else:
                        await ctx.respond(str(int(result/10)) + 'A' + str(result % 10) + 'B')

                        
                            


                elif msg.content.lower() == "stop":
                    await ctx.respond("Game ended")
                    break
                else:
                    await ctx.send("That's not a vaild input")
                    continue


                # await ctx.send(f"{msg.author}")    
                        

                
            
            # except :
            #     await ctx.send(embed =Bokai.something_is_wrong())
    
    @guess.command(description="Shows the leaderboard")
    async def leaderboard(self,ctx: discord.ApplicationContext):
        member = ctx.author.name + '#' + ctx.author.discriminator
        embed=discord.Embed(title="*Guessint Leaderboard*")
        if rank_database == {}:
            await ctx.respond("No one has played yet")
        else:
            sort_list = sorted(rank_database.keys(), reverse=True)
            for i in range(len(sort_list)):
                embed.add_field(name=sort_list[i], value=rank_database[sort_list[i]], inline=True)
            await ctx.respond(embed=embed)



    @guess.command(description="Reveals the number")
    async def debug(self,ctx: discord.ApplicationContext):
        ctx.respond(rank_database)



def setup(bot):
    bot.add_cog(guessint(bot))
 