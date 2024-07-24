import discord
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 😃')

@bot.command(name='listemojis')
async def listemojis(ctx):
    emojis = ctx.guild.emojis
    if emojis:
        emoji_list = '\n'.join([str(e) for e in emojis])
        await ctx.send(f'Custom emojis:\n{emoji_list} 😃')
    else:
        await ctx.send('No custom emojis available ❗')

@bot.command(name='addemoji')
@commands.has_permissions(manage_emojis=True)
async def addemoji(ctx, name: str, url: str):
    async with ctx.channel.typing():
        async with bot.http_session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file ❌')
            data = await resp.read()
            emoji = await ctx.guild.create_custom_emoji(name=name, image=data)
            await ctx.send(f'Emoji {emoji} created successfully ✅')

@bot.command(name='deleteemoji')
@commands.has_permissions(manage_emojis=True)
async def deleteemoji(ctx, name: str):
    emoji = get(ctx.guild.emojis, name=name)
    if emoji:
        await emoji.delete()
        await ctx.send(f'Emoji {name} deleted successfully 🗑️')
    else:
        await ctx.send('Emoji not found ❌')

@bot.command(name='steal')
@commands.has_permissions(manage_emojis=True)
async def steal(ctx, emoji: str, name: str):
    if emoji.startswith('<:') and emoji.endswith('>'):
        emoji_id = emoji.split(':')[2][:-1]
        emoji_url = f'https://cdn.discordapp.com/emojis/{emoji_id}.png'
        async with ctx.channel.typing():
            async with bot.http_session.get(emoji_url) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file ❌')
                data = await resp.read()
                new_emoji = await ctx.guild.create_custom_emoji(name=name, image=data)
                await ctx.send(f'Emoji {new_emoji} stolen and added as {name} ✅')
    else:
        await ctx.send('Invalid emoji format ❌')

@bot.command(name='emojiinfo')
async def emojiinfo(ctx, name: str):
    emoji = get(ctx.guild.emojis, name=name)
    if emoji:
        await ctx.send(f'**Emoji Info** 📜\nName: {emoji.name}\nID: {emoji.id}\nCreated at: {emoji.created_at}\nURL: {emoji.url}')
    else:
        await ctx.send('Emoji not found ❌')

@bot.command(name='helpemoji')
async def helpemoji(ctx):
    help_message = """
    **Emoji Bot Commands** 📜
    `!listemojis` - Lists all custom emojis in the server
    `!addemoji <name> <url>` - Adds a new custom emoji from a URL (Admin only)
    `!deleteemoji <name>` - Deletes a custom emoji by name (Admin only)
    `!steal <emoji> <name>` - Steals an emoji from another server and adds it to this server (Admin only)
    `!emojiinfo <name>` - Displays information about a custom emoji
    """
    await ctx.send(help_message)

bot.run('witheld')  # your api key
