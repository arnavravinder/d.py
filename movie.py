import discord
from discord.ext import commands
import openai
import json

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

OPENAI_API_KEY = 'witheld'  # your api key
openai.api_key = OPENAI_API_KEY

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 🎬')

@bot.command(name='recommendmovie')
async def recommendmovie(ctx, *, preferences: str):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Recommend a movie based on these preferences: {preferences}",
            max_tokens=100
        )
        recommendation = response.choices[0].text.strip()
        await ctx.send(f'Movie Recommendation: {recommendation} 🎥')
    except Exception as e:
        await ctx.send(f'Error: {str(e)} ❌')

@bot.command(name='moviegenre')
async def moviegenre(ctx, *, genre: str):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Recommend a movie in the genre: {genre}",
            max_tokens=100
        )
        recommendation = response.choices[0].text.strip()
        await ctx.send(f'{genre.capitalize()} Movie Recommendation: {recommendation} 🎥')
    except Exception as e:
        await ctx.send(f'Error: {str(e)} ❌')

@bot.command(name='topmovies')
async def topmovies(ctx, year: int):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"List the top movies of {year}",
            max_tokens=150
        )
        top_movies = response.choices[0].text.strip()
        await ctx.send(f'Top Movies of {year} 🎬:\n{top_movies}')
    except Exception as e:
        await ctx.send(f'Error: {str(e)} ❌')

@bot.command(name='movieinfo')
async def movieinfo(ctx, *, title: str):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Provide information about the movie: {title}",
            max_tokens=150
        )
        info = response.choices[0].text.strip()
        await ctx.send(f'Information about {title} 🎬:\n{info}')
    except Exception as e:
        await ctx.send(f'Error: {str(e)} ❌')

@bot.command(name='moviehelp')
async def moviehelp(ctx):
    help_message = """
    **Movie Recommendation Bot Commands** 📜
    `!recommendmovie <preferences>` - Recommends a movie based on user preferences
    `!moviegenre <genre>` - Recommends a movie in a specific genre
    `!topmovies <year>` - Lists the top movies of a specific year
    `!movieinfo <title>` - Provides information about a specific movie
    """
    await ctx.send(help_message)

bot.run('witheld')  # your api key
