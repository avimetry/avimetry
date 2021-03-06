"""
Commands to manage your server (Limited, Might Remove.)
Copyright (C) 2021 avizum

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import discord

from utils import core
from typing import Union
from discord.ext import commands
from utils import AvimetryBot, AvimetryContext, ModReason


class ServerManagement(commands.Cog, name="Server Management"):
    def __init__(self, bot: AvimetryBot):
        self.bot = bot

    @core.command(
        aliases=["members", "mc"], brief="Gets the members of the server and shows you."
    )
    async def membercount(self, ctx: AvimetryContext):
        tmc = len([m for m in ctx.guild.members if not m.bot])
        tbc = len([m for m in ctx.guild.members if m.bot])
        amc = ctx.guild.member_count
        mce = discord.Embed(title=f"Member Count for {ctx.guild.name}")
        mce.add_field(name="Members:", value=f"{tmc} members", inline=False)
        mce.add_field(name="Bots:", value=f"{tbc} bots", inline=False)
        mce.add_field(name="Total Members:", value=f"{amc} members", inline=False)
        await ctx.send(embed=mce)

    @core.group(invoke_without_command=True)
    @core.has_permissions(manage_channels=True)
    @core.bot_has_permissions(manage_channels=True)
    async def channel(self, ctx):
        await ctx.send_help(ctx.command)

    @channel.group(invoke_without_command=True)
    @core.has_permissions(manage_channels=True)
    @core.bot_has_permissions(manage_channels=True)
    async def create(self, ctx: AvimetryContext):
        await ctx.send_help(ctx.command)

    @create.command(aliases=["tc", "text", "textchannel", "text-channel"])
    @core.has_permissions(manage_channels=True)
    @core.bot_has_permissions(manage_channels=True)
    async def text_channel(self, ctx: AvimetryContext, name):
        channel = await ctx.guild.create_text_channel(name)
        await ctx.send(f"Created channel {channel.mention}.")

    @create.command(aliases=["vc", "voice", "voicechannel", "voice-channel"])
    @core.has_permissions(manage_channels=True)
    @core.bot_has_permissions(manage_channels=True)
    async def voice_channel(self, ctx: AvimetryContext, name):
        channel = await ctx.guild.create_voice_channel(name)
        await ctx.send(f"Created channel {channel.mention}.")

    @create.command()
    @core.has_permissions(manage_channels=True)
    @core.bot_has_permissions(manage_channels=True)
    async def category(self, ctx: AvimetryContext, name):
        channel = await ctx.guild.create_text_channel(name)
        await ctx.send(f"Created category channel {channel.mention}.")

    @channel.command()
    @core.has_permissions(manage_channels=True)
    @core.bot_has_permissions(manage_channels=True)
    async def clone(self, ctx: AvimetryContext, channel: Union[discord.CategoryChannel,
                                                               discord.TextChannel,
                                                               discord.VoiceChannel,
                                                               discord.StageChannel]):
        if isinstance(channel, discord.CategoryChannel):
            new = await channel.clone()
            for channels in channel.channels:
                thing = await channels.clone(reason="because")
                await thing.edit(category=new)
            return await ctx.send(f"Successfully cloned {channel.mention}.")
        await channel.clone(reason="because")
        await ctx.send(f"Successfully cloned {channel.mention}.")

    @channel.command()
    @core.has_permissions(manage_channels=True)
    @core.bot_has_permissions(manage_channels=True)
    async def delete(self, ctx: AvimetryContext, channel: Union[discord.CategoryChannel,
                                                                discord.TextChannel,
                                                                discord.VoiceChannel,
                                                                discord.StageChannel]):

        conf = await ctx.confirm(f"Are you sure you want to delete {channel.mention}?")
        if conf:
            return await ctx.channel.delete()
        return await ctx.send('Aborted.')

    @core.command(aliases=["steal-emoji", "stealemoji"])
    @core.has_permissions(manage_emojis=True)
    @core.bot_has_permissions(manage_emojis=True)
    async def steal_emoji(self, ctx: AvimetryContext, emoji: discord.PartialEmoji, *, reason: ModReason = None):
        asset = await emoji.url.read()
        await ctx.guild.create_custom_emoji(name=emoji.name, image=asset, reason=reason)

    @core.command()
    @core.has_permissions(manage_roles=True)
    @core.bot_has_permissions(manage_roles=True)
    async def create_role(self, ctx: AvimetryContext, name: str, color: discord.Color = None, reason: ModReason = None):
        await ctx.guild.create_role(name=name, color=color, reason=reason)


def setup(bot):
    bot.add_cog(ServerManagement(bot))
