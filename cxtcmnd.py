import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

commands_file = 'custom_commands.json'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ✨')
    load_custom_commands()

def load_custom_commands():
    try:
        with open(commands_file, 'r') as f:
            custom_commands = json.load(f)
        for name, response in custom_commands.items():
            create_command(name, response)
    except FileNotFoundError:
        with open(commands_file, 'w') as f:
            json.dump({}, f)

def save_custom_command(name, response):
    with open(commands_file, 'r') as f:
        custom_commands = json.load(f)
    custom_commands[name] = response
    with open(commands_file, 'w') as f:
        json.dump(custom_commands, f, indent=4)

def remove_custom_command(name):
    with open(commands_file, 'r') as f:
        custom_commands = json.load(f)
    if name in custom_commands:
        del custom_commands[name]
    with open(commands_file, 'w') as f:
        json.dump(custom_commands, f, indent=4)

def create_command(name, response):
    @bot.command(name=name)
    async def custom_command(ctx):
        await ctx.send(response)

    bot.add_command(custom_command)

@bot.command(name='addcommand')
@commands.has_permissions(administrator=True)
async def addcommand(ctx, name: str, *, response: str):
    save_custom_command(name, response)
    create_command(name, response)
    await ctx.send(f'Custom command `{name}` added! ✨')

@bot.command(name='removecommand')
@commands.has_permissions(administrator=True)
async def removecommand(ctx, name: str):
    remove_custom_command(name)
    command = bot.get_command(name)
    if command:
        bot.remove_command(name)
    await ctx.send(f'Custom command `{name}` removed! 🗑️')

@bot.command(name='listcommands')
async def listcommands(ctx):
    with open(commands_file, 'r') as f:
        custom_commands = json.load(f)
    if custom_commands:
        commands_list = '\n'.join([f'`{name}`' for name in custom_commands.keys()])
        await ctx.send(f'Custom commands:\n{commands_list} 📜')
    else:
        await ctx.send('No custom commands available ❗')

@bot.command(name='helpcommands')
async def helpcommands(ctx):
    help_message = """
    **Custom Commands Bot Commands** 📜
    `!addcommand <name> <response>` - Adds a new custom command (Admin only)
    `!removecommand <name>` - Removes a custom command (Admin only)
    `!listcommands` - Lists all custom commands
    """
    await ctx.send(help_message)

bot.run('witheld')  # your api key
