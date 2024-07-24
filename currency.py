import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

EXCHANGE_API_KEY = 'witheld'  # your api key
EXCHANGE_API_URL = 'https://openexchangerates.org/api/latest.json'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 💱')

@bot.command(name='exchange')
async def exchange(ctx, base: str, target: str, amount: float):
    try:
        params = {'app_id': EXCHANGE_API_KEY, 'base': base.upper()}
        response = requests.get(EXCHANGE_API_URL, params=params).json()
        if 'error' in response:
            await ctx.send('Error fetching exchange rate ❌')
            return
        rate = response['rates'].get(target.upper())
        if rate is None:
            await ctx.send('Invalid target currency ❌')
            return
        converted_amount = rate * amount
        await ctx.send(f'{amount} {base.upper()} is {converted_amount:.2f} {target.upper()} 💱')
    except Exception as e:
        await ctx.send(f'Error: {str(e)} ❌')

@bot.command(name='exchangerate')
async def exchangerate(ctx, base: str, target: str):
    try:
        params = {'app_id': EXCHANGE_API_KEY, 'base': base.upper()}
        response = requests.get(EXCHANGE_API_URL, params=params).json()
        if 'error' in response:
            await ctx.send('Error fetching exchange rate ❌')
            return
        rate = response['rates'].get(target.upper())
        if rate is None:
            await ctx.send('Invalid target currency ❌')
            return
        await ctx.send(f'Exchange rate: 1 {base.upper()} = {rate:.2f} {target.upper()} 💱')
    except Exception as e:
        await ctx.send(f'Error: {str(e)} ❌')

@bot.command(name='listcurrencies')
async def listcurrencies(ctx):
    try:
        params = {'app_id': EXCHANGE_API_KEY}
        response = requests.get(EXCHANGE_API_URL, params=params).json()
        if 'error' in response:
            await ctx.send('Error fetching currencies ❌')
            return
        currencies = ', '.join(response['rates'].keys())
        await ctx.send(f'Available currencies: {currencies} 💱')
    except Exception as e:
        await ctx.send(f'Error: {str(e)} ❌')

@bot.command(name='exchangehelp')
async def exchangehelp(ctx):
    help_message = """
    **Currency Exchange Bot Commands** 📜
    `!exchange <base_currency> <target_currency> <amount>` - Converts an amount from base currency to target currency
    `!exchangerate <base_currency> <target_currency>` - Provides the exchange rate from base currency to target currency
    `!listcurrencies` - Lists all available currencies
    """
    await ctx.send(help_message)

bot.run('witheld')  # your api key
