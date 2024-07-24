import discord
from discord.ext import commands, tasks
import datetime
import asyncio

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

timers = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ⏳')
    check_timers.start()

@bot.command(name='settimer')
async def settimer(ctx, time: str, *, event: str):
    try:
        end_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        if end_time <= datetime.datetime.now():
            await ctx.send('The time must be in the future ❌')
            return
        timers[event] = end_time
        await ctx.send(f'Timer set for "{event}" at {time} ⏰')
    except ValueError:
        await ctx.send('Invalid time format. Please use YYYY-MM-DD HH:MM:SS ❌')

@tasks.loop(seconds=10)
async def check_timers():
    now = datetime.datetime.now()
    to_remove = []
    for event, end_time in timers.items():
        if now >= end_time:
            for guild in bot.guilds:
                for channel in guild.text_channels:
                    if channel.name == 'timers':
                        asyncio.create_task(channel.send(f'Time is up for "{event}"! ⏰'))
            to_remove.append(event)
    for event in to_remove:
        del timers[event]

@bot.command(name='listtimers')
async def listtimers(ctx):
    if timers:
        timer_list = '\n'.join([f'"{event}" at {time}' for event, time in timers.items()])
        await ctx.send(f'Active timers:\n{timer_list} ⏰')
    else:
        await ctx.send('No active timers ❗')

@bot.command(name='removetimer')
async def removetimer(ctx, *, event: str):
    if event in timers:
        del timers[event]
        await ctx.send(f'Timer for "{event}" removed 🗑️')
    else:
        await ctx.send(f'No timer found for "{event}" ❗')

@bot.command(name='timerhelp')
async def timerhelp(ctx):
    help_message = """
    **Timer Bot Commands** 📜
    `!settimer <YYYY-MM-DD HH:MM:SS> <event>` - Sets a countdown timer for an event
    `!listtimers` - Lists all active timers
    `!removetimer <event>` - Removes a specific timer
    """
    await ctx.send(help_message)

@bot.command(name='setcountdown')
async def setcountdown(ctx, seconds: int, *, event: str):
    if seconds <= 0:
        await ctx.send('The countdown time must be greater than zero ❌')
        return
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    timers[event] = end_time
    await ctx.send(f'Countdown set for "{event}" in {seconds} seconds ⏰')

bot.run('witheld')  # your api key
