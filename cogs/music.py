import os

import discord
from discord.ext import commands

from utils import log, web


class Music(commands.Cog):
    """
    Play music from YouTube videos, directly with a link or by searching.
    """

    def __init__(self, bot):
        self.bot = bot
        self.voice_channels = {}

        for file in os.listdir("data"):
            if file.endswith(".mp3"):
                os.remove(f"data/{file}")

    @commands.command()
    async def join(self, ctx):
        """Join the room occupied by the person invoking the command.
           usage: !join"""
        if ctx.author.voice:
            if (
                not ctx.voice_client
                or ctx.author.voice.channel != ctx.voice_client.channel
            ):
                self.voice_channels[
                    ctx.message.guild.id
                ] = await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not in any voice channel!")

    @commands.command()
    async def play(self, ctx, *, video):
        """Play music from a YouTube video"""
        await self.join(ctx)

        if web.url_validator(video):
            web.youtube_download(video)

        self.voice_channels[ctx.message.guild.id].play(
            discord.FFmpegPCMAudio("data/audio.mp3")
        )

    @commands.command()
    async def skip(self, ctx):
        """Skip the current playing video"""
        pass

    @commands.command(aliases=["stop"])
    async def pause(self, ctx):
        """Pause the current playing video"""
        self.voice_channels[ctx.message.guild.id].pause()

    @commands.command(aliases=["resume"])
    async def unpause(self, ctx):
        """Unpause the currently paused video"""
        self.voice_channels[ctx.message.guild.id].resume()

    @commands.command()
    async def leave(self, ctx):
        """Leave the current voice channel"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(Music(bot))
