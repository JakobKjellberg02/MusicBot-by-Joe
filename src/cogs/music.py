import discord
from discord import app_commands
from discord.ext import commands

from util.audioSource import AudioSource
from view.musicPlayerView import MusicPlayerView

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.audio_source_manager = AudioSource()
        self.player_message = None

    async def play_next(self, interaction):
        guild_id = interaction.guild_id
        
        if not self.queue.get(guild_id):
            await interaction.guild.voice_client.disconnect()
            return

        source = self.queue[guild_id][0]
        interaction.guild.voice_client.play(
            source,
            after=lambda e: self.bot.loop.create_task(self.song_finished(interaction))
        )
        
        if self.player_message:
            await self.player_message.delete()  

        embed = discord.Embed(title="Now Playing", description=source.title)
        embed.set_thumbnail(url=source.thumbnail)
        view = MusicPlayerView(self)  
        self.player_message = await interaction.followup.send(embed=embed, view=view)

    async def song_finished(self, interaction):
        guild_id = interaction.guild_id

        if guild_id in self.queue and self.queue[guild_id]:
            self.queue[guild_id].pop(0)

        if self.queue.get(guild_id):
            await self.play_next(interaction)
        else:
            await interaction.guild.voice_client.disconnect()

    @app_commands.command(name="play", description="Start or add a song to the music player")
    async def play(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer()

        if interaction.channel.name != 'music':
            return await interaction.followup.send("You can only use music commands in #music.")

        if not interaction.user.voice:
            return await interaction.followup.send("You must be in a voice channel.")

        voice_channel = interaction.user.voice.channel
        if not interaction.guild.voice_client:
            await voice_channel.connect()

        try:
            source = await self.audio_source_manager.get_audio_source_yt(url)
            if not source:
                return await interaction.followup.send("Couldn't retrieve the audio source.")
        except Exception as e:
            return await interaction.followup.send(f"Error retrieving audio: {str(e)}.")

        guild_id = interaction.guild_id
        if guild_id not in self.queue:
            self.queue[guild_id] = []

        self.queue[guild_id].append(source)

        if len(self.queue[guild_id]) == 1:
            await self.play_next(interaction)

        await interaction.followup.send(f"Added to queue: {source.title}.")

    async def skip(self, interaction: discord.Interaction):
        await interaction.response.defer()  

        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()
            await interaction.followup.send("Song skipped.")
        else:
            await interaction.followup.send("No song is currently playing.")

    async def stop(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        if interaction.guild.voice_client:
            self.queue[guild_id].clear()
            interaction.guild.voice_client.stop()
            await interaction.guild.voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Music(bot))
