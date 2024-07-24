import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

BOOKS_API_KEY = 'witheld'  # your api key
BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 📚')

@bot.command(name='recommend')
async def recommend(ctx, *, genre: str):
    params = {'q': f'subject:{genre}', 'key': BOOKS_API_KEY, 'maxResults': 5}
    response = requests.get(BOOKS_API_URL, params=params).json()
    if 'items' not in response:
        await ctx.send('No books found for this genre ❌')
    else:
        books = response['items']
        book_list = ''
        for book in books:
            title = book['volumeInfo'].get('title', 'No title')
            authors = ', '.join(book['volumeInfo'].get('authors', ['Unknown author']))
            description = book['volumeInfo'].get('description', 'No description')
            book_list += f'**Title:** {title}\n**Authors:** {authors}\n**Description:** {description}\n\n'
        await ctx.send(f'Books in genre {genre}:\n{book_list} 📚')

@bot.command(name='searchbook')
async def searchbook(ctx, *, query: str):
    params = {'q': query, 'key': BOOKS_API_KEY, 'maxResults': 5}
    response = requests.get(BOOKS_API_URL, params=params).json()
    if 'items' not in response:
        await ctx.send('No books found for this query ❌')
    else:
        books = response['items']
        book_list = ''
        for book in books:
            title = book['volumeInfo'].get('title', 'No title')
            authors = ', '.join(book['volumeInfo'].get('authors', ['Unknown author']))
            description = book['volumeInfo'].get('description', 'No description')
            book_list += f'**Title:** {title}\n**Authors:** {authors}\n**Description:** {description}\n\n'
        await ctx.send(f'Search results for "{query}":\n{book_list} 📚')

@bot.command(name='bookhelp')
async def bookhelp(ctx):
    help_message = """
    **Book Recommendation Bot Commands** 📜
    `!recommend <genre>` - Recommends books based on genre
    `!searchbook <query>` - Searches for books based on a query
    """
    await ctx.send(help_message)

@bot.command(name='recommendrandom')
async def recommendrandom(ctx):
    genres = ['fiction', 'mystery', 'fantasy', 'science fiction', 'non-fiction', 'romance', 'horror']
    genre = random.choice(genres)
    params = {'q': f'subject:{genre}', 'key': BOOKS_API_KEY, 'maxResults': 5}
    response = requests.get(BOOKS_API_URL, params=params).json()
    if 'items' not in response:
        await ctx.send('No books found for this genre ❌')
    else:
        books = response['items']
        book_list = ''
        for book in books:
            title = book['volumeInfo'].get('title', 'No title')
            authors = ', '.join(book['volumeInfo'].get('authors', ['Unknown author']))
            description = book['volumeInfo'].get('description', 'No description')
            book_list += f'**Title:** {title}\n**Authors:** {authors}\n**Description:** {description}\n\n'
        await ctx.send(f'Randomly recommended books in genre {genre}:\n{book_list} 📚')

@bot.command(name='recommendbytitle')
async def recommendbytitle(ctx, *, title: str):
    params = {'q': f'intitle:{title}', 'key': BOOKS_API_KEY, 'maxResults': 5}
    response = requests.get(BOOKS_API_URL, params=params).json()
    if 'items' not in response:
        await ctx.send('No books found for this title ❌')
    else:
        books = response['items']
        book_list = ''
        for book in books:
            title = book['volumeInfo'].get('title', 'No title')
            authors = ', '.join(book['volumeInfo'].get('authors', ['Unknown author']))
            description = book['volumeInfo'].get('description', 'No description')
            book_list += f'**Title:** {title}\n**Authors:** {authors}\n**Description:** {description}\n\n'
        await ctx.send(f'Recommendations for title "{title}":\n{book_list} 📚')

@bot.command(name='recommendbyauthor')
async def recommendbyauthor(ctx, *, author: str):
    params = {'q': f'inauthor:{author}', 'key': BOOKS_API_KEY, 'maxResults': 5}
    response = requests.get(BOOKS_API_URL, params=params).json()
    if 'items' not in response:
        await ctx.send('No books found for this author ❌')
    else:
        books = response['items']
        book_list = ''
        for book in books:
            title = book['volumeInfo'].get('title', 'No title')
            authors = ', '.join(book['volumeInfo'].get('authors', ['Unknown author']))
            description = book['volumeInfo'].get('description', 'No description')
            book_list += f'**Title:** {title}\n**Authors:** {authors}\n**Description:** {description}\n\n'
        await ctx.send(f'Recommendations for author "{author}":\n{book_list} 📚')

bot.run('witheld')  # your api key
