from discord.ext import commands
from utility_functions.GPT import gptReply


class GPTCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_channel = None

    def arrangeMes(self, message):
        role = 'user' if message.author != self.bot.user else 'assistant'
        mes = message.content.replace('/gpt ', '') if message.author != self.bot.user \
            else message.content.split(':\n', 1)[1]
        return {'role': role, 'content': mes}

    async def reply(self, ctx, messages, mesAuthor=None):
        author = ctx.message.author.mention if mesAuthor is None else mesAuthor.mention
        ans = await ctx.send(f'{author}:' + '\n' + 'Ожидайте')
        reply = gptReply(messages)
        await ans.edit(content=f'{author}:' + '\n' + reply)

    @commands.command(name='gpt')
    async def gpt(self, ctx, *, message):
        print('Запрос был отправлен и обрабатывается.')
        if ctx.channel == self.bot_channel:
            new_thread = await ctx.channel.create_thread(
                name='bot ' + '_'.join(message.split()[:3]) + ' ' + str(ctx.message.author),
                message=ctx.message,
                auto_archive_duration=4320  # 3 days
            )
            await self.reply(new_thread, [self.arrangeMes(ctx.message)], ctx.message.author)
        elif ctx.channel.name.startswith('bot '):
            messages = [message async for message in ctx.channel.history(limit=200) if
                        message.content.startswith('/gpt ')
                        or message.author == self.bot.user][:-1]
            messages.append(await ctx.channel.parent.fetch_message(ctx.channel.id))
            messages.reverse()
            messages = list(map(self.arrangeMes, messages))
            print(messages)
            await self.reply(ctx, messages)

    @commands.command()
    async def initChannel(self, ctx):
        if self.bot_channel is None:
            self.bot_channel = ctx.channel
            await ctx.channel.purge(limit=1)
            await ctx.send('Канал был установлен')
        else:
            await ctx.send(f'Канал уже установлен: {self.bot_channel}')

    @commands.command()
    async def thanks(self, ctx):
        if ctx.channel.name.startswith('bot '):
            await ctx.channel.delete()
            firstMes = await ctx.channel.parent.fetch_message(ctx.channel.id)
            await firstMes.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(GPTCommands(bot))
    print("GPT DLC has loaded")
