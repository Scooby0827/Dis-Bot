import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import yt_dlp

with open('token.txt','w') as file:
    file.write("MTIyMDk1NDMxNDU3OTc3NTQ5OA.GKb6ZW.E4QuyQuTEWETPW5JH_mfgt0woLIsJAe9eO379I")
print("Token written over")

with open('token.txt','r')as file:
    first_line = file.readline()
    
with open('firstline.txt','w') as new_file:
    new_file.write(first_line)
    
print('First line is copied')

# Initializes the bot with the command prefix '!' and all intents enabled.
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')

# Prints a message in the console when the bot is successfully connected to Discord.
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Defines a command '!join' that allows the bot to join the voice channel of the user invoking the command.
@client.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send('You need to be in a channel for the bot to work')
        return
    voice_channel = ctx.author.voice.channel
    if ctx.guild.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

# Defines a command '!disconnect' that allows the bot to disconnect from the voice channel it's currently in.
@client.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()

# Defines a command '!play' that plays audio from a given URL in the voice channel the bot is in.
@client.command()
async def play(ctx, url):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            return
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    ydl_options = {
        'format': 'bestaudio/best',
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'url' in info:
            audio_url = info['url']
            # Fetches audio from the provided URL and plays it in the voice channel.
            source = await discord.FFmpegOpusAudio.from_probe(audio_url, executable=r"C:\PATH_Programs\bin\ffmpeg.exe", **FFMPEG_OPTIONS)
            ctx.voice_client.play(source)
        else:
            await ctx.send("Failed to retrieve audio from the provided URL.")

# Defines a command '!resume' that resumes playback of audio in the voice channel.
@client.command()
async def resume(ctx):
    ctx.voice_client.resume()
    await ctx.send('Resumed')

# Defines a command '!pause' that pauses playback of audio in the voice channel.
@client.command()
async def pause(ctx):
    await ctx.voice_client.pause()
    await ctx.send('Paused')

# Runs the bot with the provided token. 
client.run(first_line)

