import discord
import yt_dlp
import asyncio

class AudioSource:
    def __init__(self):
        self.ytdl_format_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
        }

        self.ffmpeg_options = {
            'options': '-vn',
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        }
        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_format_options)

    async def get_audio_source_yt(self, url):
        try:
            info = await asyncio.to_thread(self.ytdl.extract_info, url, download=False)
            if 'url' not in info:
                print(f"The audio URL was invalid")
                return None
            
            audio_url = info['url']
            if not audio_url:
                print(f"Audio URL is empty")
                return None
            
            audio_source = discord.FFmpegOpusAudio(
                audio_url, 
                **self.ffmpeg_options
            )

            return audio_source
        except Exception as e:
            print(f"Error retrieving the audio: {e}")
            return None