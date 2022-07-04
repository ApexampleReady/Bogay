

from datetime import datetime

from logging import exception
from time import time
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
import Bokai


todo_database = {}

# Initializing up Modal input of /todo add to use later in the commands
class Modal_Input_of_Add(discord.ui.Modal):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.add_item(discord.ui.InputText(label="Todo Name",placeholder="Name of this todo:"))
        self.add_item(discord.ui.InputText(label="DeadLine",placeholder="Format: YYYY-MM-DD"))



    async def callback(self, interaction: discord.Interaction):  #Actions to do when user input 
        member = interaction.user # Getting the user created the todo
        username = member.name + '#' + member.discriminator
        print(username)
        try:
            time = datetime.strptime(str(self.children[1].value),'%Y-%m-%d')
        except:
            time = datetime.strptime('9999-12-31','%Y-%m-%d')
        name = self.children[0].value
        now = datetime.now()
        print(username in todo_database)
        try:
            if time < now:
                await interaction.response.send_message("You can't create a deadline in the past XD")
            elif username not in todo_database:
                todo_database[username] = {}
                
             # add check for todo name already exists
            todo_database[username][name] = {'time':time}
            #     todo_database[member.name].append({name: time})
        except exception as e:
            await interaction.response.send_message(embed = Bokai.messages.something_is_wrong())
            print(e)
        try:
            embed = discord.Embed(title="Modal Results")
            embed.add_field(name="Todo Name", value=self.children[0].value)
            embed.add_field(name="DeadLine", value=self.children[1].value)
            embed.add_field(name="Member", value=member)
            embed.add_field(name="dictionary",value = todo_database)
            await interaction.response.send_message(embeds=[embed])
        except:
            pass

# Initializing the Button Class to use in /todo clear command
class Confirmation_Button(discord.ui.View):
    @discord.ui.button(label="Are you sure to clear all your todos",style= discord.ButtonStyle.blurple,emoji = '‼')
    async def button_callback(self,button,interaction):
        member = interaction.user.name + '#' + interaction.user.discriminator
        button.disabled = True # Disable the button
        
        if member not in todo_database:
            button.label = "It seems that you don't have any todos"
            button.emoji = "🛑"
            button.style = discord.ButtonStyle.red
            await interaction.response.edit_message(view=self)
        else:
            try:
                button.label = "All of your todos are cleared"
                button.emoji = "✅"
                button.style = discord.ButtonStyle.green
                await interaction.response.edit_message(view=self) # Edit the message's view
                del todo_database[member]
                # await interaction.response.send_message("All of you todos are cleared")
            except:
                await interaction.response.send_message(embed = Bokai.messages.something_is_wrong())


class Delete_all_button(discord.ui.View):
    @discord.ui.button(label="Are you sure to delete all todos",style= discord.ButtonStyle.red,emoji = '🗑')
    async def button_callback(self,button,interaction):
        global todo_database
        member = interaction.user.name + '#' + interaction.user.discriminator
        button.disabled = True # Disable the button
        button.label = "All of your todos are deleted"
        button.emoji = "✅"
        button.style = discord.ButtonStyle.green
        await interaction.response.edit_message(view=self) # Edit the message's view

        todo_database = {}
        
    
        


# Initializing this Cog
class todo(commands.Cog):
    def __init__(self,bot):
        self.bot = bot



    todo_list = SlashCommandGroup("todo","Commands of the todo module")
# description="Command to access the todo module"
    
    @todo_list.command(description="Shows all the todo commands in the todo module")
    async def help(self,ctx: discord.ApplicationContext):
        embed=discord.Embed(title="*Todo Commands*")
        embed.add_field(name="/todo add [name]:", value="Adds a new item to list     ", inline=True)
        embed.add_field(name="/todo delete [name]", value="Remove a item from list", inline=True)
        embed.add_field(name="/todo show [name]", value="Show all items in order", inline=True)
        embed.add_field(name="/todo clear", value="Clear all items", inline=True)
        await ctx.respond(embed=embed)
    

    @todo_list.command(description="Adds a new item to list")
    async def add(self,ctx: discord.ApplicationContext):
        name = ""
        modal = Modal_Input_of_Add(title = "Todo Creation")
        await ctx.send_modal(modal)

        # if ctx == "":
        #     await ctx.respond("Please enter a name")
            
        # if name in self.bot.todo:
        #     await ctx.respond("This item already exists")
        #     return
        # self.bot.todo.append("asd")
        # await ctx.send("I think you fucked up")
        # await ctx.respond(f"{ctx} has been added to the list")


    @todo_list.command(description = "Remove a item from list")
    async def delete(self,ctx: discord.ApplicationContext, name: str):
        member = ctx.author.name + '#' + ctx.author.discriminator # Getting the user created the todo
        exists = False
        # for i in range(len(todo_database[member])):
        #     if name in todo_database[member][i]:
        #         exists = True
        #         index = i
        #         break
        if name in todo_database[member]:
            try: 
                del todo_database[member][name]
                await ctx.respond(f"{name} has been deleted")
            except:
                await ctx.respond(embed = Bokai.messages.something_is_wrong())
        else:
            await ctx.respond('This todo does not exist, please try again')
    
    @todo_list.command(description = "Show all your todos in order")
    async def show(self, ctx:discord.ApplicationContext):
        member = ctx.author.name + '#' + ctx.author.discriminator
        print(member)
        embed=discord.Embed(title="*Your Todos*")
        
        if member not in todo_database:

            embed=discord.Embed()
            embed.add_field(name="❌Error", value="It seems that you didn't create any todos yet", inline=False)
            await ctx.respond(embed=embed)
        else:
            sort_list = sorted(todo_database[member].items(), key=lambda x: x[1]['time'])
            # for i in todo_database[member]:
            #     pass
            
            # for key in todo_database[member].keys():
            for i in range(len(sort_list)):
                embed.add_field(name=sort_list[i][0], value=sort_list[i][1]['time'].strftime("%Y-%m-%d"), inline=False)
                # embed.add_field(name= key ,value=todo_database[member][key]['time'].strftime("%Y-%m-%d"))
            await ctx.respond(embed=embed)
    
    @todo_list.command(description = "Clear all your todos")
    async def clear(self,ctx:discord.ApplicationContext):
        await ctx.respond(view=Confirmation_Button())
    
    @todo_list.command(description = "Clear the entire todo database")
    async def clearall(self,ctx:discord.ApplicationContext):
        await ctx.respond(view=Delete_all_button())


    @todo_list.command(description = "Shows the todo database")
    async def debug(self,ctx:discord.ApplicationContext):
        await ctx.respond(todo_database)
        

def setup(bot):
    bot.add_cog(todo(bot))
 