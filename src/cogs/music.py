import discord
from discord.ext import commands

from util.audioSource import AudioSource

class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.queue = {}
        self.audio_source_manager = AudioSource()

        @commands.command(name='play')
        async def play(self, ctx, *, url):
            if not ctx.author.voice:
                return await ctx.send(f"You must be in a voice channel.")
            
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            
            source = await self.audio_source.get_audio_source_yt(url)
            if not source:
                return await ctx.send(f"Couldn't retrieve the audio source")
            
            guild_id = ctx.guild.id
            if guild_id not in self.queue:
                self.queue[guild_id] = []

            self.queue[guild_id].append(source)

            if len(self.queue[guild_id]) == 1:
                await self.play_next(ctx)
            
            await ctx.send(f"Added to queue: {url}")

async def setup(bot):
    await bot.add_cog(Music(bot))


          