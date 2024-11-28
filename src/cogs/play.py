import discord
from discord import app_commands
from discord.ext import commands

from util.audioSource import AudioSource

class PlayCommand(commands.Cog):
    def __init__(self, bot, music_manager):
        self.bot = bot
        self.music_manager = music_manager
        self.audio_source_manager = AudioSource()

    @app_commands.command(name="play", description="Play a song from YouTube")
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
            return await interaction.followup.send(f"Error retrieving audio: {str(e)}")

        guild_id = interaction.guild_id
        if guild_id not in self.music_manager.queue:
            self.music_manager.queue[guild_id] = []

        self.music_manager.queue[guild_id].append(source)

        if len(self.music_manager.queue[guild_id]) == 1:
            await self.music_manager.play_next(interaction)

        await interaction.followup.send(f"Added to queue: {url}")
    