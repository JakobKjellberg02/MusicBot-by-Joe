import discord
from discord import app_commands
from discord.ext import commands

class SkipCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="skip", description="Skip the current song")
    async def skip(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if not interaction.guild.voice_client:
            return await interaction.followup.send("Not in a voice channel.")

        if not interaction.guild.voice_client.is_playing():
            return await interaction.followup.send("Not currently playing a song.")

        interaction.guild.voice_client.stop()
        await interaction.followup.send("Skipped the current song.")
