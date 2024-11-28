import discord
from discord import ui, app_commands
from discord.ext import commands

class MusicPlayerView(ui.View):
    def __init__(self, cog):
        super().__init__()
        self.cog = cog
        self.current_page = 0

    @ui.button(label="⏯️ Pause/Resume", style=discord.ButtonStyle.primary)
    async def pause_resume(self, interaction: discord.Interaction, button: ui.Button):
        voice_client = interaction.guild.voice_client
        if voice_client:
            if voice_client.is_playing():
                voice_client.pause()
                button.label = "▶️ Resume"
            elif voice_client.is_paused():
                voice_client.resume()
                button.label = "⏸️ Pause"
            await interaction.response.edit_message(view=self)

    @ui.button(label="⏭️ Skip", style=discord.ButtonStyle.secondary)
    async def skip(self, interaction: discord.Interaction, button: ui.Button):
        await self.cog.skip(interaction)

    @ui.button(label="⏹️ Stop", style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, button: ui.Button):
        await self.cog.stop(interaction)