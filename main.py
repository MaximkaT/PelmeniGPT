import discord
from discord.ext import commands
from GPT import gptReply
from keys import botKey, AIkey
import openai

# Permissions for the bot
intents = discord.Intents.all()
# Bot itself
bot = commands.Bot(command_prefix="/", intents=intents)
# Key that allows you to use ChatGPT
openai.api_key = AIkey

messages = {}  # Previous Discord messages


# Checking if the bot is ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


# Main command that receives your message and sends you a reply to it
@bot.command(name='chat', description='Send a prompt to the bot')
async def chat(context, *, message):
    # message - your message
    user = context.author  # User's name
    reply = gptReply(messages, user, message)  # Function that returns a reply for your message
    await context.send(f'{user}:' + '\n' + reply)  # Send reply as a discord message with username as a label


# Command to reset your message history if needed
@bot.command(name='resetHistory', description="Resets the history of your and bot's messages")
async def resetHistory(ctx):
    messages[ctx.author] = []


bot.run(botKey)  # Bot launch
