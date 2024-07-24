import discord
from discord.ext import commands, tasks
import datetime
import json

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

birthdays_file = 'birthdays.json'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 🎉')
    birthday_check.start()

def load_birthdays():
    try:
        with open(birthdays_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_birthdays(birthdays):
    with open(birthdays_file, 'w') as f:
        json.dump(birthdays, f, indent=4)

@bot.command(name='setbirthday')
async def setbirthday(ctx, date: str):
    try:
        birthday = datetime.datetime.strptime(date, '%Y-%m-%d')
        birthdays = load_birthdays()
        birthdays[str(ctx.author.id)] = date
        save_birthdays(birthdays)
        await ctx.send(f'Birthday set for {ctx.author.mention} on {date} 🎂')
    except ValueError:
        await ctx.send('Invalid date format. Please use YYYY-MM-DD ❌')

@bot.command(name='getbirthday')
async def getbirthday(ctx, member: discord.Member = None):
    member = member or ctx.author
    birthdays = load_birthdays()
    if str(member.id) in birthdays:
        await ctx.send(f'{member.mention}\'s birthday is on {birthdays[str(member.id)]} 🎉')
    else:
        await ctx.send(f'Birthday not set for {member.mention} ❗')

@tasks.loop(hours=24)
async def birthday_check():
    await bot.wait_until_ready()
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    birthdays = load_birthdays()
    for guild in bot.guilds:
        for member in guild.members:
            if str(member.id) in birthdays and birthdays[str(member.id)] == today:
                for channel in guild.text_channels:
                    if channel.name == 'birthdays':
                        await channel.send(f'Happy Birthday {member.mention}! 🎉🎂')

@bot.command(name='removebirthday')
async def removebirthday(ctx):
    birthdays = load_birthdays()
    if str(ctx.author.id) in birthdays:
        del birthdays[str(ctx.author.id)]
        save_birthdays(birthdays)
        await ctx.send(f'Birthday removed for {ctx.author.mention} 🗑️')
    else:
        await ctx.send(f'Birthday not set for {ctx.author.mention} ❗')

@bot.command(name='listbirthdays')
async def listbirthdays(ctx):
    birthdays = load_birthdays()
    if birthdays:
        birthday_list = '\n'.join([f'{ctx.guild.get_member(int(uid)).mention}: {date}' for uid, date in birthdays.items() if ctx.guild.get_member(int(uid))])
        await ctx.send(f'Birthdays:\n{birthday_list} 📅')
    else:
        await ctx.send('No birthdays set ❗')

@bot.command(name='birthdayhelp')
async def birthdayhelp(ctx):
    help_message = """
    **Birthday Bot Commands** 📜
    `!setbirthday <YYYY-MM-DD>` - Sets your birthday
    `!getbirthday [member]` - Gets the birthday of a member (or yourself if no member specified)
    `!removebirthday` - Removes your birthday
    `!listbirthdays` - Lists all set birthdays
    """
    await ctx.send(help_message)

bot.run('witheld')  # your api key
