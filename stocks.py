import discord
from discord.ext import commands, tasks
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

STOCK_API_KEY = 'witheld'  # your api key
STOCK_API_URL = 'https://www.alphavantage.co/query'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 📈')
    stock_update.start()

@bot.command(name='stockprice')
async def stockprice(ctx, symbol: str):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': STOCK_API_KEY
    }
    response = requests.get(STOCK_API_URL, params=params).json()
    try:
        last_refreshed = response['Meta Data']['3. Last Refreshed']
        price = response['Time Series (1min)'][last_refreshed]['1. open']
        await ctx.send(f'The current price of {symbol.upper()} is ${price} 📈')
    except KeyError:
        await ctx.send('Error fetching stock price ❌')

@bot.command(name='stockinfo')
async def stockinfo(ctx, symbol: str):
    params = {
        'function': 'OVERVIEW',
        'symbol': symbol,
        'apikey': STOCK_API_KEY
    }
    response = requests.get(STOCK_API_URL, params=params).json()
    try:
        name = response['Name']
        description = response['Description']
        market_cap = response['MarketCapitalization']
        await ctx.send(f'**{name}** 📊\n{description}\nMarket Cap: ${market_cap}')
    except KeyError:
        await ctx.send('Error fetching stock information ❌')

@bot.command(name='marketupdate')
async def marketupdate(ctx):
    params = {
        'function': 'SECTOR',
        'apikey': STOCK_API_KEY
    }
    response = requests.get(STOCK_API_URL, params=params).json()
    try:
        sectors = response['Rank A: Real-Time Performance']
        update = '\n'.join([f'{sector}: {performance}' for sector, performance in sectors.items()])
        await ctx.send(f'**Market Update** 📊\n{update}')
    except KeyError:
        await ctx.send('Error fetching market update ❌')

@tasks.loop(hours=1)
async def stock_update():
    await bot.wait_until_ready()
    channel = discord.utils.get(bot.get_all_channels(), name='stock-updates')
    if channel:
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': 'AAPL',
            'interval': '1min',
            'apikey': api key
        }
        response = requests.get(STOCK_API_URL, params=params).json()
        try:
            last_refreshed = response['Meta Data']['3. Last Refreshed']
            price = response['Time Series (1min)'][last_refreshed]['1. open']
            await channel.send(f'The current price of AAPL is ${price} 📈')
        except KeyError:
            await channel.send('Error fetching stock price ❌')

@bot.command(name='stockhelp')
async def stockhelp(ctx):
    help_message = """
    **Stock Price Bot Commands** 📜
    `!stockprice <symbol>` - Fetches the current stock price for a given symbol
    `!stockinfo <symbol>` - Provides information about a specific stock
    `!marketupdate` - Provides a real-time market update
    """
    await ctx.send(help_message)

stock_update.start()

bot.run('witheld')  # your api key
