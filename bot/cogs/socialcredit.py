import pathlib
import json
import discord
from  discord.ext import commands

class Credit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "social credit"

    @commands.command(name = "sc", description = "check the current social credit of a user")
    async def sc_command(self, ctx, name: str):
        await ctx.send("hh")

def setup(bot):
    bot.add_cog(Credit(bot))