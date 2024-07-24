import discord
from discord.ext import commands, tasks
import datetime
import json

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

events_file = 'events.json'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 🎉')
    check_events.start()

def load_events():
    try:
        with open(events_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_events(events):
    with open(events_file, 'w') as f:
        json.dump(events, f, indent=4)

@bot.command(name='scheduleevent')
@commands.has_permissions(administrator=True)
async def scheduleevent(ctx, date: str, time: str, *, event_name: str):
    event_datetime = f'{date} {time}'
    try:
        event_time = datetime.datetime.strptime(event_datetime, '%Y-%m-%d %H:%M:%S')
        events = load_events()
        events[event_name] = {
            'time': event_time.strftime('%Y-%m-%d %H:%M:%S'),
            'author': str(ctx.author)
        }
        save_events(events)
        await ctx.send(f'Event "{event_name}" scheduled for {event_datetime} 🗓️')
    except ValueError:
        await ctx.send('Invalid date/time format. Use YYYY-MM-DD and HH:MM:SS ❌')

@tasks.loop(minutes=1)
async def check_events():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    events = load_events()
    for event_name, details in list(events.items()):
        if now >= details['time']:
            channel = bot.get_channel(details['channel_id'])
            if channel:
                asyncio.create_task(channel.send(f'Event "{event_name}" is happening now! 🎉'))
            del events[event_name]
            save_events(events)

@bot.command(name='listevents')
async def listevents(ctx):
    events = load_events()
    if events:
        event_list = '\n'.join([f'"{name}" scheduled for {details["time"]}' for name, details in events.items()])
        await ctx.send(f'Scheduled events:\n{event_list} 🗓️')
    else:
        await ctx.send('No events scheduled ❗')

@bot.command(name='cancelevent')
@commands.has_permissions(administrator=True)
async def cancelevent(ctx, *, event_name: str):
    events = load_events()
    if event_name in events:
        del events[event_name]
        save_events(events)
        await ctx.send(f'Event "{event_name}" cancelled 🗑️')
    else:
        await ctx.send(f'Event "{event_name}" not found ❌')

@bot.command(name='eventhelp')
async def eventhelp(ctx):
    help_message = """
    **Event Bot Commands** 📜
    `!scheduleevent <YYYY-MM-DD> <HH:MM:SS> <event_name>` - Schedules an event (Admin only)
    `!listevents` - Lists all scheduled events
    `!cancelevent <event_name>` - Cancels a scheduled event (Admin only)
    """
    await ctx.send(help_message)

bot.run('witheld')  # your api key
