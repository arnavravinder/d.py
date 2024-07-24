import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

quotes_file = 'quotes.json'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 📝')

def load_quotes():
    try:
        with open(quotes_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_quotes(quotes):
    with open(quotes_file, 'w') as f:
        json.dump(quotes, f, indent=4)

@bot.command(name='addquote')
async def addquote(ctx, *, quote: str):
    quotes = load_quotes()
    quotes[str(ctx.message.id)] = {
        'author': str(ctx.author),
        'quote': quote
    }
    save_quotes(quotes)
    await ctx.send('Quote added! 📝')

@bot.command(name='quote')
async def quote(ctx, quote_id: str = None):
    quotes = load_quotes()
    if quote_id:
        if quote_id in quotes:
            await ctx.send(f'Quote: "{quotes[quote_id]["quote"]}" - {quotes[quote_id]["author"]} 📜')
        else:
            await ctx.send('Quote not found ❌')
    else:
        if quotes:
            random_id = random.choice(list(quotes.keys()))
            await ctx.send(f'Quote: "{quotes[random_id]["quote"]}" - {quotes[random_id]["author"]} 📜')
        else:
            await ctx.send('No quotes available ❗')

@bot.command(name='listquotes')
async def listquotes(ctx):
    quotes = load_quotes()
    if quotes:
        quotes_list = '\n'.join([f'ID: {i}, "{q["quote"]}" - {q["author"]}' for i, q in quotes.items()])
        await ctx.send(f'Quotes:\n{quotes_list} 📜')
    else:
        await ctx.send('No quotes available ❗')

@bot.command(name='deletequote')
@commands.has_permissions(manage_messages=True)
async def deletequote(ctx, quote_id: str):
    quotes = load_quotes()
    if quote_id in quotes:
        del quotes[quote_id]
        save_quotes(quotes)
        await ctx.send('Quote deleted! 🗑️')
    else:
        await ctx.send('Quote not found ❌')

@bot.command(name='quotehelp')
async def quotehelp(ctx):
    help_message = """
    **Quote Bot Commands** 📜
    `!addquote <quote>` - Adds a new quote
    `!quote [quote_id]` - Shows a random quote or a specific quote by ID
    `!listquotes` - Lists all stored quotes
    `!deletequote <quote_id>` - Deletes a quote by ID (Admin only)
    """
    await ctx.send(help_message)

bot.run('witheld')  # your api key
