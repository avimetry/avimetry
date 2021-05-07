import humanize
import jishaku
import discord
import sys
import psutil
from jishaku.cog import STANDARD_FEATURES, OPTIONAL_FEATURES
from jishaku import Feature
from jishaku.flags import JISHAKU_HIDE
from utils.converters import CogConverter
from utils import AvimetryBot, AvimetryContext


class Jishaku(*OPTIONAL_FEATURES, *STANDARD_FEATURES):
    """
    Advanced debug cog.
    """
    @Feature.Command(
        parent="jsk",
        name="load",
        aliases=["l"]
    )
    async def jsk_load(self, ctx: AvimetryContext, module: CogConverter):
        command = self.bot.get_command("dev load")
        await command(ctx, module=module)

    @Feature.Command(
        parent="jsk",
        name="unload",
        aliases=["u"]
    )
    async def jsk_unload(self, ctx: AvimetryContext, module: CogConverter):
        command = self.bot.get_command("dev unload")
        await command(ctx, module=module)

    @Feature.Command(
        parent="jsk",
        name="reload",
        aliases=["r"]
    )
    async def jsk_reload(self, ctx: AvimetryContext, module: CogConverter):
        command = self.bot.get_command("dev reload")
        await command(ctx, module=module)

    @Feature.Command(name="jishaku", aliases=["jsk"], hidden=JISHAKU_HIDE,
                     invoke_without_command=True, ignore_extra=False)
    async def jsk(self, ctx: AvimetryContext):
        summary = [
            f"Jishaku `v{jishaku.__version__}`, discord.py `v{discord.__version__}`, "
            f"Python `{sys.version}` on `{sys.platform}`, ".replace("\n", ""),
            f"Jishaku was loaded {humanize.naturaltime(self.load_time)} and "
            f"Jishaku cog was loaded {humanize.naturaltime(self.start_time)}.",
            ""
        ]
        try:
            proc = psutil.Process()
            with proc.oneshot():
                try:
                    mem = proc.memory_full_info()
                    summary.append(
                        f"I am using {humanize.naturalsize(mem.rss)} physical memory and "
                        f"{humanize.naturalsize(mem.vms)} virtual memory, "
                        f"{humanize.naturalsize(mem.uss)} of which is unique this this process."
                    )
                except psutil.AccessDenied:
                    pass

                try:
                    name = proc.name()
                    pid = proc.pid
                    thread_count = proc.num_threads()
                    summary.append(
                        f"I am running on Process ID `{pid}` (`{name}`) with {thread_count} threads")
                except psutil.AccessDenied:
                    pass
                summary.append("")

        except psutil.AccessDenied:
            summary.append("psutil is installed but this process does not have access to display this information")
            summary.append("")

        cache_summary = f"{len(self.bot.guilds)} guild(s) and {len(self.bot.users)} user(s)"

        if isinstance(self.bot, discord.AutoShardedClient):
            summary.append(f"I am automatically sharded and can see {cache_summary}")
        elif self.bot.shard_count:
            summary.append(f"I am manually sharded and can see {cache_summary}")
        else:
            summary.append(f"I am not sharded and can see {cache_summary}.")

        if self.bot._connection.max_messages:
            message_cache = f"Message cache is capped at {self.bot._connection.max_messages}"
        else:
            message_cache = "Message cache is not enabled"

        if discord.version_info >= (1, 5, 0):
            prescence_intent = f"`presence` intent is `{'enabled' if self.bot.intents.presences else 'disabled'}`"
            members_intent = f"`members` intent is `{'enabled' if self.bot.intents.members else 'disabled'}`"
            summary.append(f"{message_cache}, {prescence_intent} and {members_intent}")
        else:
            guild_subs = self.bot._connection.guild_subscriptions
            guild_subscriptions = f"`guild subscriptions` are `{'enabled' if guild_subs else 'disabled'}`"
            summary.append(f"{message_cache} and {guild_subscriptions}.")
        summary.append("")

        summary.append(f"Websocket latency: `{round(self.bot.latency * 1000)}ms`")

        jishaku_embed = discord.Embed(description="\n".join(summary))
        await ctx.send(embed=jishaku_embed)
    pass


def setup(avi: AvimetryBot):
    avi.add_cog(Jishaku(bot=avi))
