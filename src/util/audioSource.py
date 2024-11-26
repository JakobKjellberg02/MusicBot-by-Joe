import discord
import yt_dlp

class AudioSource:
    def __init__(self):
        self.ytdl_format_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
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
        }
        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_format_options)

        async def get_audio_source_yt(self, url):
            try:
                info = self.ytdl.extract_info(url, download=False)
                url = info['url']

                return discord.FFmpegOpusAudio(url, **self.ffmpeg_options)
            except Exception as e:
                print(f"Error retrieving the audio: {e}")
                return None