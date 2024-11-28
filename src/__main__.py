import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv() # load .env for API key
DISCORD_BOT_API_KEY = os.getenv('DISCORD_TOKEN') # Discord API key

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # discord.py logging

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# MusicBot main class
class MusicByJoe(commands.Bot):
    async def setup_hook(self):
        """ Loads commands from the cogs folder"""
        if os.path.exists('src/cogs'):
            for filename in os.listdir('src/cogs'):
                if filename.endswith('.py'):
                    try:
                        await self.load_extension(f'cogs.{filename[:-3]}')
                        print(f'Loaded extension: {filename}')
                    except Exception as e:
                        print(f'Failed to load extension {filename}: {str(e)}')
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} slash command(s)")
        except Exception as e:
            print(f"Error syncing slash commands: {str(e)}")

    async def on_ready(self):
        """ Ready check from the bot"""
        print(f'{self.user} has connected!')
        await self.change_presence(activity=discord.CustomActivity("Use / to see commands"))

def main():
    """ It is show time baby """
    bot = MusicByJoe(command_prefix=None, intents=intents) 
    bot.run(DISCORD_BOT_API_KEY, log_handler=handler)

if __name__ == "__main__": # Python main call 
    main()