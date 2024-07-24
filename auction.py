import discord
from discord.ext import commands, tasks
import asyncio
import datetime

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

auctions = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 🏷️')

class Auction:
    def __init__(self, item, starting_bid, end_time, author):
        self.item = item
        self.starting_bid = starting_bid
        self.current_bid = starting_bid
        self.end_time = end_time
        self.author = author
        self.winner = None

@bot.command(name='startauction')
@commands.has_permissions(administrator=True)
async def startauction(ctx, item: str, starting_bid: int, duration: int):
    end_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=duration)
    auctions[ctx.channel.id] = Auction(item, starting_bid, end_time, ctx.author)
    await ctx.send(f'Auction started for {item} with a starting bid of {starting_bid} 🏷️ Ends in {duration} minutes.')

@tasks.loop(seconds=10)
async def check_auctions():
    now = datetime.datetime.utcnow()
    to_remove = []
    for channel_id, auction in auctions.items():
        if now >= auction.end_time:
            channel = bot.get_channel(channel_id)
            if auction.winner:
                message = f'Auction ended! Winner: {auction.winner.mention} with a bid of {auction.current_bid} 🎉'
            else:
                message = f'Auction ended! No bids were placed for {auction.item} ❌'
            asyncio.create_task(channel.send(message))
            to_remove.append(channel_id)
    for channel_id in to_remove:
        del auctions[channel_id]

@bot.command(name='bid')
async def bid(ctx, amount: int):
    if ctx.channel.id not in auctions:
        await ctx.send('No active auction in this channel ❌')
        return

    auction = auctions[ctx.channel.id]
    if amount <= auction.current_bid:
        await ctx.send(f'Bid must be higher than the current bid of {auction.current_bid} ❗')
        return

    auction.current_bid = amount
    auction.winner = ctx.author
    await ctx.send(f'New highest bid of {amount} by {ctx.author.mention} 🏷️')

@bot.command(name='auctioninfo')
async def auctioninfo(ctx):
    if ctx.channel.id not in auctions:
        await ctx.send('No active auction in this channel ❌')
        return

    auction = auctions[ctx.channel.id]
    remaining_time = (auction.end_time - datetime.datetime.utcnow()).total_seconds() / 60
    await ctx.send(f'Auction for {auction.item}\nCurrent bid: {auction.current_bid}\nEnds in: {remaining_time:.2f} minutes\n')

@bot.command(name='cancelauction')
@commands.has_permissions(administrator=True)
async def cancelauction(ctx):
    if ctx.channel.id not in auctions:
        await ctx.send('No active auction in this channel ❌')
        return

    del auctions[ctx.channel.id]
    await ctx.send('Auction cancelled 🛑')

@bot.command(name='auctionhelp')
async def auctionhelp(ctx):
    help_message = """
    **Auction Bot Commands** 📜
    `!startauction <item> <starting_bid> <duration>` - Starts an auction (Admin only)
    `!bid <amount>` - Places a bid in the current auction
    `!auctioninfo` - Displays information about the current auction
    `!cancelauction` - Cancels the current auction (Admin only)
    """
    await ctx.send(help_message)

check_auctions.start()

bot.run('witheld')  # your api key
