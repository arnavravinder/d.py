import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

TRANSLATE_API_KEY = 'witheld'  # your api key

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} 🌐')

@bot.command(name='translate')
async def translate(ctx, target_lang: str, *, text: str):
    url = f'https://translation.googleapis.com/language/translate/v2?key={TRANSLATE_API_KEY}'
    data = {'q': text, 'target': target_lang}
    response = requests.post(url, data=data).json()
    if 'error' in response:
        await ctx.send('Translation error ❌')
    else:
        translation = response['data']['translations'][0]['translatedText']
        await ctx.send(f'Translation ({target_lang}): {translation} 🌍')

@bot.command(name='languages')
async def languages(ctx):
    url = f'https://translation.googleapis.com/language/translate/v2/languages?key={TRANSLATE_API_KEY}'
    response = requests.get(url).json()
    if 'error' in response:
        await ctx.send('Error fetching languages ❌')
    else:
        languages = response['data']['languages']
        languages_list = ', '.join([lang['language'] for lang in languages])
        await ctx.send(f'Available languages: {languages_list} 📝')

@bot.command(name='detect')
async def detect(ctx, *, text: str):
    url = f'https://translation.googleapis.com/language/translate/v2/detect?key={TRANSLATE_API_KEY}'
    data = {'q': text}
    response = requests.post(url, data=data).json()
    if 'error' in response:
        await ctx.send('Detection error ❌')
    else:
        language = response['data']['detections'][0][0]['language']
        confidence = response['data']['detections'][0][0]['confidence']
        await ctx.send(f'Detected language: {language} with confidence {confidence*100}% 🌐')

@bot.command(name='setapikey')
@commands.has_permissions(administrator=True)
async def setapikey(ctx, *, api_key: str):
    global TRANSLATE_API_KEY
    TRANSLATE_API_KEY = api_key
    await ctx.send('API key updated 🔑')

@bot.command(name='listlanguages')
async def listlanguages(ctx):
    url = f'https://translation.googleapis.com/language/translate/v2/languages?key={TRANSLATE_API_KEY}'
    response = requests.get(url).json()
    if 'error' in response:
        await ctx.send('Error fetching languages ❌')
    else:
        languages = response['data']['languages']
        languages_list = '\n'.join([lang['name'] for lang in languages])
        await ctx.send(f'Available languages:\n{languages_list} 📝')

@bot.command(name='translatehelp')
async def translatehelp(ctx):
    help_message = """
    **Translation Bot Commands** 📜
    `!translate <target_lang> <text>` - Translates text to the target language
    `!languages` - Lists available languages
    `!detect <text>` - Detects the language of the provided text
    `!setapikey <api_key>` - Sets the API key (Admin only)
    `!listlanguages` - Lists all available languages with names
    """
    await ctx.send(help_message)

bot.run('witheld')  # your api key
