import discord
from discord.ext import commands, tasks
import datetime

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 📊')
    update_stats.start()

@tasks.loop(minutes=10)
async def update_stats():
    for guild in bot.guilds:
        member_count = guild.member_count
        online_count = sum(1 for member in guild.members if member.status != discord.Status.offline)
        text_channel_count = len(guild.text_channels)
        voice_channel_count = len(guild.voice_channels)
        activity_message = (f'Server Stats 📊\n'
                            f'Members: {member_count}\n'
                            f'Online: {online_count}\n'
                            f'Text Channels: {text_channel_count}\n'
                            f'Voice Channels: {voice_channel_count}')
        for channel in guild.text_channels:
            if channel.name == 'server-stats':
                async for message in channel.history(limit=1):
                    await message.edit(content=activity_message)
                if not message:
                    await channel.send(activity_message)

@bot.command(name='membercount')
async def membercount(ctx):
    member_count = ctx.guild.member_count
    await ctx.send(f'Member count: {member_count} 👥')

@bot.command(name='onlinecount')
async def onlinecount(ctx):
    online_count = sum(1 for member in ctx.guild.members if member.status != discord.Status.offline)
    await ctx.send(f'Online members: {online_count} 🟢')

@bot.command(name='channelcount')
async def channelcount(ctx):
    text_channel_count = len(ctx.guild.text_channels)
    voice_channel_count = len(ctx.guild.voice_channels)
    await ctx.send(f'Text Channels: {text_channel_count} 📝\nVoice Channels: {voice_channel_count} 🔊')

@bot.command(name='serverinfo')
async def serverinfo(ctx):
    guild = ctx.guild
    member_count = guild.member_count
    online_count = sum(1 for member in guild.members if member.status != discord.Status.offline)
    text_channel_count = len(guild.text_channels)
    voice_channel_count = len(guild.voice_channels)
    created_at = guild.created_at.strftime('%Y-%m-%d %H:%M:%S')
    owner = guild.owner
    info_message = (f'**Server Info** 📜\n'
                    f'Name: {guild.name}\n'
                    f'Owner: {owner}\n'
                    f'Created at: {created_at}\n'
                    f'Members: {member_count}\n'
                    f'Online: {online_count}\n'
                    f'Text Channels: {text_channel_count}\n'
                    f'Voice Channels: {voice_channel_count}')
    await ctx.send(info_message)

@bot.command(name='serverage')
async def serverage(ctx):
    guild = ctx.guild
    now = datetime.datetime.utcnow()
    age = now - guild.created_at
    days = age.days
    await ctx.send(f'The server is {days} days old ⏳')

@bot.command(name='roles')
async def roles(ctx):
    roles = ', '.join([role.name for role in ctx.guild.roles if role.name != "@everyone"])
    await ctx.send(f'Roles: {roles} 🎭')

@bot.command(name='serverstats')
async def serverstats(ctx):
    guild = ctx.guild
    member_count = guild.member_count
    online_count = sum(1 for member in guild.members if member.status != discord.Status.offline)
    text_channel_count = len(guild.text_channels)
    voice_channel_count = len(guild.voice_channels)
    activity_message = (f'**Server Stats** 📊\n'
                        f'Members: {member_count}\n'
                        f'Online: {online_count}\n'
                        f'Text Channels: {text_channel_count}\n'
                        f'Voice Channels: {voice_channel_count}')
    await ctx.send(activity_message)

@bot.command(name='boosts')
async def boosts(ctx):
    boosts = ctx.guild.premium_subscription_count
    await ctx.send(f'Boosts: {boosts} 🚀')

@bot.command(name='helpstats')
async def helpstats(ctx):
    help_message = """
    **Server Stats Bot Commands** 📜
    `!membercount` - Displays the number of members
    `!onlinecount` - Displays the number of online members
    `!channelcount` - Displays the number of text and voice channels
    `!serverinfo` - Displays information about the server
    `!serverage` - Displays the age of the server
    `!roles` - Displays the roles in the server
    `!serverstats` - Displays a summary of server statistics
    `!boosts` - Displays the number of server boosts
    """
    await ctx.send(help_message)

bot.run('witheld')  # your api key
