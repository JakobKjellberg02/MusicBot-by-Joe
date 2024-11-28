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
            
            if not info or 'url' not in info:
                raise ValueError("Invalid audio source")
            
            audio_url = info['url']
            audio_source = discord.FFmpegOpusAudio(
                audio_url, 
                **self.ffmpeg_options
            )

            audio_source.url = url
            audio_source.title = info.get('title', 'Unknown Title')
            audio_source.duration = info.get('duration', 0)
            audio_source.thumbnail = info.get('thumbnail', '')
            
            return audio_source
        
        except Exception as e:
            print(f"Error retrieving audio from {url}: {e}")
            return None
