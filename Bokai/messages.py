import discord


def something_is_wrong():
    # Calls this function when something went wrong
    return discord.Embed(title="🛑 Something went wrong", description="Please this try again later", color=0x254bbb)