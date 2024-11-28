import discord
from discord import app_commands
from discord.ext import commands

class MusicManager:
    def __init__(self):
        self.queue = {}

    async def play_next(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id

        if not self.queue.get(guild_id):
            await interaction.guild.voice_client.disconnect()
            return

        source = self.queue[guild_id][0]

        interaction.guild.voice_client.play(
            source,
            after=lambda e: interaction.client.loop.create_task(self.song_finished(interaction))
        )

    async def song_finished(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id

        if guild_id in self.queue and self.queue[guild_id]:
            self.queue[guild_id].pop(0)

        if self.queue.get(guild_id):
            await self.play_next(interaction)
        else:
            await interaction.guild.voice_client.disconnect()
