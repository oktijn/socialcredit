import datetime as dt
import typing as t
from pathlib import Path
import json
import pathlib

import discord
from discord.ext import commands
from discord_components import *

class SocialCredit(commands.Cog):
    def __init__(self, bot):
        bot.remove_command("help")
        self.bot = bot
        self.description = "This cog contains the default commands."
    
    @commands.command(name="help", description="Displays the cogs or information about a cog, usage:\nCogs: ``help``\nInformation about a cog: ``help [cog]``")
    async def help_command(self, ctx, *, category: t.Optional[str]):
        embed = discord.Embed(
            title="social credit call center", 
            description="find all info about social credit here",
            color = ctx.author.color,
            timestamp = dt.datetime.utcnow(),
        )
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        buttons = []
        if category is None:
            for cog, cog_obj in self.bot.cogs.items():
                embed.add_field(
                    name=cog,
                    value=cog_obj.description,
                    inline=True
                )
                buttons.append(Button(label=cog))
        else:
            if category in self.bot.cogs:
                cog = self.bot.get_cog(category)
                for command in cog.get_commands():
                    description = "-"
                    if command.description != "":
                        description = command.description
                    embed.add_field(
                        name=command.name,
                        value=description,
                        inline=True
                    )
            else:
                await ctx.send(f"er is geen cog die ``{category}`` heet.\ndit commando is hoofdlettergevoelig dus kijk of je de hoofdletters goed hebt geschreven")
                return

        msg = await ctx.send(embed=embed, components=[buttons])

        while True:
            event = await ctx.bot.wait_for("button_click")
            if event.channel is not ctx.channel:
                return
            if event.channel == ctx.channel:
                await msg.delete()
                embed = discord.Embed(
                    title="sociale krediet hulplijn",
                    description="alle informatie over sociale krediet kan je hier vinden",
                    color = ctx.author.color,
                    timestamp = dt.datetime.utcnow()
                )
                embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                buttons = []
                cog = self.bot.get_cog(event.component.label)
                for command in cog.get_commands():
                    description = "-"
                    if command.description != "":
                        description = command.description
                    embed.add_field(
                        name=command.name,
                        value=description,
                        inline=True
                    )

def setup(bot):
    bot.add_cog(SocialCredit(bot))

class SocialCreditBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True, intents=discord.Intents.all())
    
    def setup(self):
        print("Running setup...")
        self.load_extension("bot.bot")
        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f"Loaded '{cog}' cog.")
        
        print("Setup complete.")

    def run(self):
        self.setup()

        with open("data/token.0", "r", encoding="utf-8") as f:
            token = f.read()

        print("Running bot...")
        super().run(token, reconnect=True)

    async def shutdown(self):
        print("Closing bot...")
        await super().close()

    async def close(self):
        await self.shutdown()

    async def on_connect(self):
        print(f"Bot running (latency: {self.latency*1000} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot stopped.")

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot ready.")
        dict = {}
        for guild in self.guilds:
            dict[guild.id] = {}
            for member in guild.members:
                dict[guild.id][member.id] = { "credit": 0 }
        if not pathlib.Path("credits.json").exists():
            file = open("credits.json", "w")
            file = json.dump(dict, file)

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or(".")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)
        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)