import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv

from util.musicManager import MusicManager
from util.terminalPrint import TColor

from cogs.play import PlayCommand
from cogs.skip import SkipCommand

load_dotenv() # load .env for API key
DISCORD_BOT_API_KEY = os.getenv('DISCORD_TOKEN') # Discord API key

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # discord.py logging

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# MusicBot main class
class MusicByJoe(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.music_manager = MusicManager()  
    
    async def setup_hook(self):
        """Setup cogs and other async configurations."""
        cogs = [
            (PlayCommand, [self, self.music_manager], "PlayCommand"),
            (SkipCommand, [self], "SkipCommand"),
        ]

        for cog_class, args, cog_name in cogs:
            try:
                await self.add_cog(cog_class(*args))
                print(TColor.colorize(f"Successfully loaded {cog_name}.", TColor.OK))
            except Exception as e:
                print(TColor.colorize(f"{TColor.ERR}Failed to load {cog_name}{TColor.RESET}: {str(e)}"
                    , TColor.ERR))

        try:
            await self.tree.sync()
            print("Application commands synced successfully.")
        except Exception as e:
            print(f"Failed to sync application commands: {str(e)}")

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