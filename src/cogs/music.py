import discord
from discord import app_commands
from discord.ext import commands

from util.audioSource import AudioSource

class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.queue = {}
        self.audio_source_manager = AudioSource()
    
    @app_commands.command(name="play", description="Play a song from YouTube")
    async def play(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer()

        if not interaction.user.voice:
            return await interaction.followup.send("You must be in a voice channel.")
            
        voice_channel = interaction.user.voice.channel
        try:
            voice_client = await voice_channel.connect()
        except discord.ClientException:
            voice_client = interaction.guild.voice_client
            
        try: 
            source = await self.audio_source_manager.get_audio_source_yt(url)
            if not source:
                return await interaction.followup.send("Couldn't retrieve the audio source")
        except Exception as e:
            return await interaction.followup.send(f"Error retrieving audio: {str(e)}")
            
        guild_id = interaction.guild_id
        if guild_id not in self.queue:
            self.queue[guild_id] = []

        self.queue[guild_id].append(source)

        if len(self.queue[guild_id]) == 1:
            await self.play_next(interaction)
            
        await interaction.followup.send(f"Added to queue: {url}")

async def setup(bot):
    await bot.add_cog(Music(bot))


          