import discord
from discord.ext import commands
import youtube_dl
import asyncio

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

queues = {}

def check_queue(ctx):
    if queues[ctx.guild.id]:
        url = queues[ctx.guild.id].pop(0)
        play_next(ctx, url)

def play_next(ctx, url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = discord.FFmpegOpusAudio(url2, options="-vn")
        ctx.voice_client.play(source, after=lambda e: check_queue(ctx))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='join')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command(name='leave')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.command(name='play')
async def play(ctx, url):
    if ctx.voice_client:
        if ctx.guild.id not in queues:
            queues[ctx.guild.id] = []
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = discord.FFmpegOpusAudio(url2, options="-vn")
            if not ctx.voice_client.is_playing():
                ctx.voice_client.play(source, after=lambda e: check_queue(ctx))
            else:
                queues[ctx.guild.id].append(url)
                await ctx.send("Added to queue.")
    else:
        await ctx.send("I need to be in a voice channel to play music.")

@bot.command(name='pause')
async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
    else:
        await ctx.send("No audio is playing.")

@bot.command(name='resume')
async def resume(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
    else:
        await ctx.send("The audio is not paused.")

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    else:
        await ctx.send("No audio is playing.")

@bot.command(name='skip')
async def skip(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Skipped the current track.")
    else:
        await ctx.send("No audio is playing.")

@bot.command(name='queue')
async def queue(ctx):
    if ctx.guild.id in queues and queues[ctx.guild.id]:
        queue_list = "\n".join(queues[ctx.guild.id])
        await ctx.send(f"Current queue:\n{queue_list}")
    else:
        await ctx.send("The queue is empty.")

@bot.command(name='volume')
async def volume(ctx, vol: int):
    if ctx.voice_client:
        ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source)
        ctx.voice_client.source.volume = vol / 100
        await ctx.send(f"Volume set to {vol}%")
    else:
        await ctx.send("I'm not connected to a voice channel.")

@bot.command(name='clearqueue')
async def clearqueue(ctx):
    if ctx.guild.id in queues:
        queues[ctx.guild.id].clear()
        await ctx.send("Cleared the queue.")
    else:
        await ctx.send("The queue is already empty.")

bot.run('witheld')
