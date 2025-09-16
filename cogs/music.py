import discord
from discord.ext import commands
from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()  # Load API keys from .env

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

ffmpeg_options = {
    'options': '-vn'
}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def search_spotify(self, query):
        result = spotify.search(q=query, type='track', limit=1)
        items = result['tracks']['items']
        if items:
            track = items[0]
            return {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'preview_url': track['preview_url'],  # 30-sec mp3
                'external_url': track['external_urls']['spotify']
            }
        return None

    def search_youtube(self, query):
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        request = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=1
        )

        response = request.execute()
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_title = response['items'][0]['snippet']['title']

        return video_url, video_title

    @commands.command(name="play")
    async def play(self, ctx, *, search: str):
        if not ctx.author.voice:
            await ctx.send("❌ You must be in a voice channel first.")
            return

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        vc = ctx.voice_client

        track_info = self.search_spotify(search)

        if track_info and track_info['preview_url']:
            source = discord.FFmpegPCMAudio(track_info['preview_url'], **ffmpeg_options)
            track_desc = f"🎧 Playing Spotify Preview: **{track_info['name']}** by **{track_info['artist']}**"
        else:
            video_url, video_title = self.search_youtube(search)
            source = discord.FFmpegPCMAudio(video_url, **ffmpeg_options)
            track_desc = f"▶️ Playing from YouTube: **{video_title}**"

        if not vc.is_playing():
            vc.play(source, after=lambda e: print(f"Finished playback: {e}"))
            await ctx.send(track_desc)
        else:
            await ctx.send("⚠️ Already playing something.")

    @commands.command(name="stop")
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("⏹️ Stopped playback and disconnected.")

async def setup(bot):
    await bot.add_cog(Music(bot))
