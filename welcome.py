import discord
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 🎉')

@bot.event
async def on_member_join(member):
    channel = get(member.guild.text_channels, name='welcome')
    if channel:
        await channel.send(f'Welcome to the server, {member.mention}! 🎉')
    role = get(member.guild.roles, name='New Member')
    if role:
        await member.add_roles(role)
        await channel.send(f'{member.mention} has been given the {role.name} role. 🎖️')

@bot.command(name='setwelcome')
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, *, channel_name: str):
    channel = get(ctx.guild.text_channels, name=channel_name)
    if channel:
        with open('welcome_channel.txt', 'w') as f:
            f.write(str(channel.id))
        await ctx.send(f'Welcome channel set to {channel.mention} 📩')
    else:
        await ctx.send(f'Channel {channel_name} not found ❗')

@bot.command(name='setrole')
@commands.has_permissions(administrator=True)
async def setrole(ctx, *, role_name: str):
    role = get(ctx.guild.roles, name=role_name)
    if role:
        with open('welcome_role.txt', 'w') as f:
            f.write(str(role.id))
        await ctx.send(f'Welcome role set to {role.name} 🎖️')
    else:
        await ctx.send(f'Role {role_name} not found ❗')

@bot.event
async def on_member_join(member):
    with open('welcome_channel.txt', 'r') as f:
        channel_id = int(f.read().strip())
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(f'Welcome to the server, {member.mention}! 🎉')

    with open('welcome_role.txt', 'r') as f:
        role_id = int(f.read().strip())
    role = get(member.guild.roles, id=role_id)
    if role:
        await member.add_roles(role)
        await channel.send(f'{member.mention} has been given the {role.name} role. 🎖️')

@bot.command(name='welcomemsg')
@commands.has_permissions(administrator=True)
async def welcomemsg(ctx, *, message: str):
    with open('welcome_message.txt', 'w') as f:
        f.write(message)
    await ctx.send('Welcome message updated ✅')

@bot.event
async def on_member_join(member):
    with open('welcome_channel.txt', 'r') as f:
        channel_id = int(f.read().strip())
    channel = bot.get_channel(channel_id)
    if channel:
        with open('welcome_message.txt', 'r') as f:
            welcome_message = f.read().strip()
        await channel.send(f'{welcome_message}, {member.mention}! 🎉')

    with open('welcome_role.txt', 'r') as f:
        role_id = int(f.read().strip())
    role = get(member.guild.roles, id=role_id)
    if role:
        await member.add_roles(role)
        await channel.send(f'{member.mention} has been given the {role.name} role. 🎖️')

@bot.command(name='info')
async def info(ctx):
    with open('welcome_channel.txt', 'r') as f:
        channel_id = int(f.read().strip())
    channel = bot.get_channel(channel_id)
    
    with open('welcome_role.txt', 'r') as f:
        role_id = int(f.read().strip())
    role = get(ctx.guild.roles, id=role_id)

    await ctx.send(f'Welcome Channel: {channel.mention} 📩\nWelcome Role: {role.name} 🎖️')

@bot.command(name='testwelcome')
@commands.has_permissions(administrator=True)
async def testwelcome(ctx):
    with open('welcome_message.txt', 'r') as f:
        welcome_message = f.read().strip()
    await ctx.send(f'{welcome_message}, {ctx.author.mention}! 🎉')

@bot.event
async def on_member_remove(member):
    channel = get(member.guild.text_channels, name='goodbye')
    if channel:
        await channel.send(f'Goodbye {member.mention}, we will miss you! 😢')

@bot.command(name='setgoodbye')
@commands.has_permissions(administrator=True)
async def setgoodbye(ctx, *, channel_name: str):
    channel = get(ctx.guild.text_channels, name=channel_name)
    if channel:
        with open('goodbye_channel.txt', 'w') as f:
            f.write(str(channel.id))
        await ctx.send(f'Goodbye channel set to {channel.mention} 📩')
    else:
        await ctx.send(f'Channel {channel_name} not found ❗')

@bot.event
async def on_member_remove(member):
    with open('goodbye_channel.txt', 'r') as f:
        channel_id = int(f.read().strip())
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(f'Goodbye {member.mention}, we will miss you! 😢')

bot.run('witheld')
