import discord
from discord.ext import commands, tasks
import openai
import random

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

openai.api_key = 'apikey' # enter ur openai api key here
trivia_categories = ['Science', 'History', 'Geography', 'Sports', 'Entertainment']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 🧠')

@bot.command(name='starttrivia')
async def starttrivia(ctx):
    category = random.choice(trivia_categories)
    question = get_trivia_question(category)
    if question:
        await ctx.send(f'Category: {category} 📚\nQuestion: {question["question"]} ❓')
        await store_trivia_answer(ctx.channel.id, question["answer"])

def get_trivia_question(category):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Generate a trivia question and answer for the category: {category}",
        max_tokens=100
    )
    text = response.choices[0].text.strip().split('\n')
    if len(text) >= 2:
        return {"question": text[0], "answer": text[1]}
    return None

async def store_trivia_answer(channel_id, answer):
    with open(f'{channel_id}_trivia.txt', 'w') as f:
        f.write(answer)

async def get_trivia_answer(channel_id):
    try:
        with open(f'{channel_id}_trivia.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

@bot.command(name='answer')
async def answer(ctx, *, user_answer: str):
    correct_answer = await get_trivia_answer(ctx.channel.id)
    if correct_answer:
        if user_answer.lower() == correct_answer.lower():
            await ctx.send(f'Correct! 🎉 The answer was: {correct_answer}')
        else:
            await ctx.send(f'Incorrect. ❌ The correct answer was: {correct_answer}')
    else:
        await ctx.send('No active trivia question. Start a new game with !starttrivia.')

@bot.command(name='categories')
async def categories(ctx):
    await ctx.send(f'Trivia Categories: {", ".join(trivia_categories)} 📚')

@bot.command(name='addcategory')
@commands.has_permissions(administrator=True)
async def addcategory(ctx, *, category: str):
    if category not in trivia_categories:
        trivia_categories.append(category)
        await ctx.send(f'Category {category} added. ✅')
    else:
        await ctx.send(f'Category {category} already exists. ❗')

@bot.command(name='removecategory')
@commands.has_permissions(administrator=True)
async def removecategory(ctx, *, category: str):
    if category in trivia_categories:
        trivia_categories.remove(category)
        await ctx.send(f'Category {category} removed. ✅')
    else:
        await ctx.send(f'Category {category} not found. ❗')

@bot.command(name='listcategories')
async def listcategories(ctx):
    await ctx.send(f'Available categories: {", ".join(trivia_categories)} 📚')

@bot.command(name='skip')
async def skip(ctx):
    await ctx.send('Skipping the current trivia question. ⏭️')
    await store_trivia_answer(ctx.channel.id, '')

@tasks.loop(minutes=5)
async def auto_trivia():
    for guild in bot.guilds:
        category = random.choice(trivia_categories)
        question = get_trivia_question(category)
        if question:
            channel = random.choice(guild.text_channels)
            await channel.send(f'Category: {category} 📚\nQuestion: {question["question"]} ❓')
            await store_trivia_answer(channel.id, question["answer"])

@bot.command(name='startautotrivia')
@commands.has_permissions(administrator=True)
async def startautotrivia(ctx):
    auto_trivia.start()
    await ctx.send('Automatic trivia started. 🕹️')

@bot.command(name='stopautotrivia')
@commands.has_permissions(administrator=True)
async def stopautotrivia(ctx):
    auto_trivia.stop()
    await ctx.send('Automatic trivia stopped. 🛑')

@bot.command(name='setapikey')
@commands.has_permissions(administrator=True)
async def setapikey(ctx, *, api_key: str):
    openai.api_key = api_key
    await ctx.send('OpenAI API key updated. 🔑')

@bot.command(name='help')
async def help(ctx):
    help_message = """
    **Trivia Bot Commands** 📜
    `!starttrivia` - Starts a trivia game
    `!answer <your answer>` - Submit your answer
    `!categories` - Lists trivia categories
    `!addcategory <category>` - Adds a new category (Admin only)
    `!removecategory <category>` - Removes a category (Admin only)
    `!listcategories` - Lists available categories
    `!skip` - Skips the current trivia question
    `!startautotrivia` - Starts automatic trivia (Admin only)
    `!stopautotrivia` - Stops automatic trivia (Admin only)
    `!setapikey <API key>` - Sets the OpenAI API key (Admin only)
    """
    await ctx.send(help_message)

bot.run('witheld')
