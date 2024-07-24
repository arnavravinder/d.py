import discord
from discord.ext import commands
import subprocess
import os
import uuid

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 💻')

@bot.command(name='sharecode')
async def sharecode(ctx, language: str, *, code: str):
    snippet_id = str(uuid.uuid4())
    with open(f'snippets/{snippet_id}.{language}', 'w') as f:
        f.write(code)
    await ctx.send(f'Code snippet saved! Use `!runcode {snippet_id} {language}` to run it 📝')

@bot.command(name='runcode')
async def runcode(ctx, snippet_id: str, language: str):
    file_path = f'snippets/{snippet_id}.{language}'
    if not os.path.exists(file_path):
        await ctx.send('Code snippet not found ❌')
        return

    try:
        if language == 'python':
            result = subprocess.run(['python', file_path], capture_output=True, text=True, timeout=10)
        elif language == 'javascript':
            result = subprocess.run(['node', file_path], capture_output=True, text=True, timeout=10)
        else:
            await ctx.send('Unsupported language ❌')
            return

        output = result.stdout or result.stderr
        await ctx.send(f'Output:\n```\n{output}\n```')
    except subprocess.TimeoutExpired:
        await ctx.send('Execution timed out ⏳')
    except Exception as e:
        await ctx.send(f'Error: {str(e)} ❌')

@bot.command(name='deletecode')
@commands.has_permissions(manage_messages=True)
async def deletecode(ctx, snippet_id: str, language: str):
    file_path = f'snippets/{snippet_id}.{language}'
    if os.path.exists(file_path):
        os.remove(file_path)
        await ctx.send(f'Code snippet {snippet_id} deleted 🗑️')
    else:
        await ctx.send('Code snippet not found ❌')

@bot.command(name='listcode')
async def listcode(ctx):
    files = os.listdir('snippets')
    if files:
        snippet_list = '\n'.join([f'{f.split(".")[0]}.{f.split(".")[1]}' for f in files])
        await ctx.send(f'Available code snippets:\n{snippet_list} 📝')
    else:
        await ctx.send('No code snippets available ❗')

@bot.command(name='codehelp')
async def codehelp(ctx):
    help_message = """
    **Code Snippet Bot Commands** 📜
    `!sharecode <language> <code>` - Shares a code snippet
    `!runcode <snippet_id> <language>` - Executes a code snippet
    `!deletecode <snippet_id> <language>` - Deletes a code snippet (Admin only)
    `!listcode` - Lists all saved code snippets
    """
    await ctx.send(help_message)

@bot.event
async def on_ready():
    if not os.path.exists('snippets'):
        os.makedirs('snippets')

bot.run('witheld')  # your api key
