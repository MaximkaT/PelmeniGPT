import discord
from discord.ext import commands
import openai
import os
import aiohttp
import dotenv

dotenv.load_dotenv()

# Key that allows you to use ChatGPT
openai.api_key = str(os.getenv("AIkey"))


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=discord.Intents.all())
        self.initial_extensions = [
            'bot_commands.gpt_commands'
        ]

    async def setup_hook(self):
        # self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print(f"We have logged in as {self.user}")


bot = MyBot()
bot.run(str(os.getenv("BOTkey")))