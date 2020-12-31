import discord
import os
import json
import asyncio
from discord.ext import commands

class OnReady(commands.Cog):
    def __init__(self, avimetry):
        self.avimetry = avimetry
    
    async def status_task(self):
        while True:
            await self.avimetry.change_presence(activity=discord.Game('Need Help? | a.help'))
            await asyncio.sleep(60)
            await self.avimetry.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for commands'))
            await asyncio.sleep(60)
            await self.avimetry.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="'a.'"))
            await asyncio.sleep(60)
            await self.avimetry.change_presence(activity=discord.Game('discord.gg/zpj46np'))
            await asyncio.sleep(60)
            await self.avimetry.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='Sleeping Battles'))
            await asyncio.sleep(60)

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Game(f"{self.avimetry.user.name} is online!")
        await self.avimetry.change_presence(status=discord.Status.idle, activity=game)
        print('------')
        print('Succesfully logged in as')
        print(f"Username: {self.avimetry.user.name}")
        print(f"UserID: {self.avimetry.user.id}")
        print('------')
        await asyncio.sleep(5)
        self.avimetry.loop.create_task(self.status_task())

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.message.delete()
        sd=discord.Embed()
        sd.add_field(name="Shutting Down", value=f"You called the shutdown command, {self.avimetry.user.name} is now shutting down.")
        await ctx.send(embed=sd)
        await self.avimetry.change_presence(activity=discord.Game('Shutting down'))
        await asyncio.sleep(5)
        await self.avimetry.logout()

def setup(avimetry):
    avimetry.add_cog(OnReady((avimetry)))