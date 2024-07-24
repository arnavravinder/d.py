import discord
from discord.ext import commands, tasks
import datetime

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

polls = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 📊')

@bot.command(name='poll')
async def poll(ctx, *, question: str):
    message = await ctx.send(f'📊 **Poll:** {question}')
    await message.add_reaction('👍')
    await message.add_reaction('👎')
    poll_id = message.id
    polls[poll_id] = {'question': question, 'author': ctx.author, 'time': datetime.datetime.now()}
    await ctx.send(f'Poll created with ID: {poll_id} ✅')

@bot.command(name='polloptions')
async def polloptions(ctx, question: str, *options):
    if len(options) > 10:
        await ctx.send('You can only provide up to 10 options ❗')
    else:
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        poll_message = f'📊 **Poll:** {question}\n\n'
        for i, option in enumerate(options):
            poll_message += f'{reactions[i]} {option}\n'
        message = await ctx.send(poll_message)
        poll_id = message.id
        for i in range(len(options)):
            await message.add_reaction(reactions[i])
        polls[poll_id] = {'question': question, 'options': options, 'author': ctx.author, 'time': datetime.datetime.now()}
        await ctx.send(f'Poll created with ID: {poll_id} ✅')

@bot.command(name='closepoll')
async def closepoll(ctx, poll_id: int):
    poll = polls.get(poll_id)
    if poll and poll['author'] == ctx.author:
        message = await ctx.fetch_message(poll_id)
        results = {}
        for reaction in message.reactions:
            results[reaction.emoji] = reaction.count - 1
        if 'options' in poll:
            poll_results = f'Poll Results for: {poll["question"]}\n'
            for i, option in enumerate(poll['options']):
                poll_results += f'{option}: {results[reaction.emoji]} votes\n'
        else:
            poll_results = f'Poll Results for: {poll["question"]}\n👍: {results["👍"]} votes\n👎: {results["👎"]} votes\n'
        await ctx.send(poll_results)
        del polls[poll_id]
    else:
        await ctx.send('Poll not found or you are not the author of this poll ❌')

@bot.command(name='listpolls')
async def listpolls(ctx):
    if polls:
        poll_list = "Active Polls:\n"
        for poll_id, poll in polls.items():
            poll_list += f'ID: {poll_id}, Question: {poll["question"]}, Created by: {poll["author"].mention}, Created at: {poll["time"]}\n'
        await ctx.send(poll_list)
    else:
        await ctx.send('No active polls ❗')

@tasks.loop(minutes=60)
async def clear_old_polls():
    now = datetime.datetime.now()
    for poll_id, poll in list(polls.items()):
        if (now - poll['time']).days > 1:
            del polls[poll_id]

@bot.command(name='pollhelp')
async def pollhelp(ctx):
    help_message = """
    **Poll Bot Commands** 📜
    `!poll <question>` - Create a simple poll with thumbs up and thumbs down
    `!polloptions <question> <option1> <option2> ...` - Create a poll with up to 10 options
    `!closepoll <poll_id>` - Close a poll and display results (only the poll creator can close)
    `!listpolls` - List all active polls
    """
    await ctx.send(help_message)

clear_old_polls.start()

bot.run('witheld')  # your api key
