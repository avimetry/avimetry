import discord
from discord.ext import commands


class Test(commands.Cog):

    @commands.command(extras=dict(bot_perms='administrator', user_perms='manage_guild'))
    async def test_command(self, ctx: commands.Context):
        await ctx.send('nice')


def setup(bot):
    bot.add_cog(Test(bot))
