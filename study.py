import discord
from discord.ext import commands, tasks
import datetime
import json

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

study_groups_file = 'study_groups.json'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 📚')
    check_sessions.start()

def load_study_groups():
    try:
        with open(study_groups_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_study_groups(study_groups):
    with open(study_groups_file, 'w') as f:
        json.dump(study_groups, f, indent=4)

@bot.command(name='creategroup')
async def creategroup(ctx, *, group_name: str):
    study_groups = load_study_groups()
    if group_name in study_groups:
        await ctx.send('Study group already exists ❌')
    else:
        study_groups[group_name] = {
            'members': [],
            'sessions': []
        }
        save_study_groups(study_groups)
        await ctx.send(f'Study group "{group_name}" created successfully 📚')

@bot.command(name='joingroup')
async def joingroup(ctx, *, group_name: str):
    study_groups = load_study_groups()
    if group_name in study_groups:
        if ctx.author.id not in study_groups[group_name]['members']:
            study_groups[group_name]['members'].append(ctx.author.id)
            save_study_groups(study_groups)
            await ctx.send(f'You joined the study group "{group_name}" ✅')
        else:
            await ctx.send('You are already a member of this study group ❗')
    else:
        await ctx.send('Study group not found ❌')

@bot.command(name='leavegroup')
async def leavegroup(ctx, *, group_name: str):
    study_groups = load_study_groups()
    if group_name in study_groups:
        if ctx.author.id in study_groups[group_name]['members']:
            study_groups[group_name]['members'].remove(ctx.author.id)
            save_study_groups(study_groups)
            await ctx.send(f'You left the study group "{group_name}" ❌')
        else:
            await ctx.send('You are not a member of this study group ❗')
    else:
        await ctx.send('Study group not found ❌')

@bot.command(name='schedule')
async def schedule(ctx, group_name: str, date: str, time: str, *, topic: str):
    event_datetime = f'{date} {time}'
    try:
        event_time = datetime.datetime.strptime(event_datetime, '%Y-%m-%d %H:%M:%S')
        study_groups = load_study_groups()
        if group_name in study_groups:
            study_groups[group_name]['sessions'].append({
                'time': event_time.strftime('%Y-%m-%d %H:%M:%S'),
                'topic': topic
            })
            save_study_groups(study_groups)
            await ctx.send(f'Session on "{topic}" scheduled for {event_datetime} in group "{group_name}" 🗓️')
        else:
            await ctx.send('Study group not found ❌')
    except ValueError:
        await ctx.send('Invalid date/time format. Use YYYY-MM-DD and HH:MM:SS ❌')

@tasks.loop(minutes=1)
async def check_sessions():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    study_groups = load_study_groups()
    for group_name, group in study_groups.items():
        for session in list(group['sessions']):
            if now >= session['time']:
                for member_id in group['members']:
                    member = bot.get_user(member_id)
                    if member:
                        asyncio.create_task(member.send(f'Session on "{session["topic"]}" in group "{group_name}" is starting now! 🎉'))
                group['sessions'].remove(session)
                save_study_groups(study_groups)

@bot.command(name='listsessions')
async def listsessions(ctx, *, group_name: str):
    study_groups = load_study_groups()
    if group_name in study_groups:
        sessions = study_groups[group_name]['sessions']
        if sessions:
            session_list = '\n'.join([f'{s["time"]}: {s["topic"]}' for s in sessions])
            await ctx.send(f'Scheduled sessions for group "{group_name}":\n{session_list} 🗓️')
        else:
            await ctx.send('No sessions scheduled ❗')
    else:
        await ctx.send('Study group not found ❌')

@bot.command(name='listgroups')
async def listgroups(ctx):
    study_groups = load_study_groups()
    if study_groups:
        group_list = '\n'.join([f'{name} ({len(group["members"])} members)' for name, group in study_groups.items()])
        await ctx.send(f'Study groups:\n{group_list} 📚')
    else:
        await ctx.send('No study groups available ❗')

@bot.command(name='studyhelp')
async def studyhelp(ctx):
    help_message = """
    **Study Group Bot Commands** 📜
    `!creategroup <group_name>` - Creates a new study group
    `!joingroup <group_name>` - Joins an existing study group
    `!leavegroup <group_name>` - Leaves a study group
    `!schedule <group_name> <YYYY-MM-DD> <HH:MM:SS> <topic>` - Schedules a study session
    `!listsessions <group_name>` - Lists all scheduled sessions for a group
    `!listgroups` - Lists all study groups
    """
    await ctx.send(help_message)

check_sessions.start()

bot.run('witheld')  # your api key
