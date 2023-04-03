import discord
from discord.ext import commands
import openai
from keys import botKey, AIkey

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)
openai.api_key = AIkey

messages = {}


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.command()
async def chat(ctx, *, message):
    user = ctx.author
    try:
        messages[user] += [{'role': 'user', 'content': message}]
    except KeyError:
        messages[user] = []
        messages[user] += [{'role': 'user', 'content': message}]
    history = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages[user])
    reply = history.choices[0].message.content
    messages[user] += [{'role': 'assistant', 'content': reply}]
    await ctx.send(f'{user}:')
    await ctx.send(reply)


@bot.command()
async def resetHistory(ctx):
    messages[ctx.author] = []


bot.run(botKey)
