import discord
from discord.ext import commands, tasks
import datetime

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

reminders = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ⏰')
    check_reminders.start()

@bot.command(name='setreminder')
async def setreminder(ctx, time: str, *, message: str):
    user_id = ctx.author.id
    if user_id not in reminders:
        reminders[user_id] = []
    
    reminder_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    reminders[user_id].append((reminder_time, message))
    await ctx.send(f'Reminder set for {time} 📅')

@tasks.loop(seconds=60)
async def check_reminders():
    now = datetime.datetime.now()
    for user_id, user_reminders in reminders.items():
        for reminder in user_reminders:
            reminder_time, message = reminder
            if now >= reminder_time:
                user = await bot.fetch_user(user_id)
                await user.send(f'Reminder: {message} ⏰')
                user_reminders.remove(reminder)

@bot.command(name='listreminders')
async def listreminders(ctx):
    user_id = ctx.author.id
    if user_id in reminders and reminders[user_id]:
        reminder_list = "\n".join([f'{r[0].strftime("%Y-%m-%d %H:%M")}: {r[1]}' for r in reminders[user_id]])
        await ctx.send(f'Your reminders:\n{reminder_list} 📅')
    else:
        await ctx.send('You have no reminders set. ❗')

@bot.command(name='clearreminders')
async def clearreminders(ctx):
    user_id = ctx.author.id
    if user_id in reminders:
        reminders[user_id].clear()
        await ctx.send('All reminders cleared. 🗑️')
    else:
        await ctx.send('You have no reminders to clear. ❗')

@bot.command(name='reminderhelp')
async def reminderhelp(ctx):
    help_message = """
    **Reminder Bot Commands** 📜
    `!setreminder <YYYY-MM-DD HH:MM> <message>` - Sets a reminder
    `!listreminders` - Lists all your reminders
    `!clearreminders` - Clears all your reminders
    """
    await ctx.send(help_message)

@bot.command(name='removereminder')
async def removereminder(ctx, time: str):
    user_id = ctx.author.id
    if user_id in reminders:
        reminder_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
        reminder_to_remove = None
        for reminder in reminders[user_id]:
            if reminder[0] == reminder_time:
                reminder_to_remove = reminder
                break
        if reminder_to_remove:
            reminders[user_id].remove(reminder_to_remove)
            await ctx.send(f'Reminder for {time} removed. ✅')
        else:
            await ctx.send(f'No reminder found for {time}. ❗')
    else:
        await ctx.send('You have no reminders to remove. ❗')

@bot.command(name='updatereminder')
async def updatereminder(ctx, old_time: str, new_time: str, *, new_message: str):
    user_id = ctx.author.id
    if user_id in reminders:
        old_reminder_time = datetime.datetime.strptime(old_time, '%Y-%m-%d %H:%M')
        new_reminder_time = datetime.datetime.strptime(new_time, '%Y-%m-%d %H:%M')
        for reminder in reminders[user_id]:
            if reminder[0] == old_reminder_time:
                reminders[user_id].remove(reminder)
                reminders[user_id].append((new_reminder_time, new_message))
                await ctx.send(f'Reminder updated to {new_time} 📅')
                return
        await ctx.send(f'No reminder found for {old_time}. ❗')
    else:
        await ctx.send('You have no reminders to update. ❗')

@bot.command(name='snoozereminder')
async def snoozereminder(ctx, time: str, minutes: int):
    user_id = ctx.author.id
    if user_id in reminders:
        reminder_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
        new_reminder_time = reminder_time + datetime.timedelta(minutes=minutes)
        for reminder in reminders[user_id]:
            if reminder[0] == reminder_time:
                reminder_message = reminder[1]
                reminders[user_id].remove(reminder)
                reminders[user_id].append((new_reminder_time, reminder_message))
                await ctx.send(f'Reminder snoozed to {new_reminder_time.strftime("%Y-%m-%d %H:%M")} ⏰')
                return
        await ctx.send(f'No reminder found for {time}. ❗')
    else:
        await ctx.send('You have no reminders to snooze. ❗')

bot.run('witheld')
