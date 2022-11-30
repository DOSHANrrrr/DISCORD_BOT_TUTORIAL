import asyncio
import discord
import json
import qrcode
from discord.ext import commands
import os

file_for_config = open('config.json', 'r')
config = json.load(file_for_config)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(config['prefix'], intents=intents)


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'{ctx.author.mention} pong!')


@bot.command(name='foo')
async def foo(ctx: commands.context, *, args):
    result = str(args)
    await ctx.send(embed=discord.Embed(title=f'{result}', description="Hi, this is a test command", color=0x64ff0a))


@bot.command(name='qr')
async def make_qr_code(ctx, *, args):
    file_name = str(args).replace(' ', '_')

    img = qrcode.make(file_name + '.png')

    try:
        img.save(file_name + '.png')
    except Exception as e:
        print(e)

    await ctx.send(file=discord.File(os.path.abspath(file_name + '.png')))

    os.remove(os.path.abspath(file_name + '.png'))


async def load_cogs():
    for file in os.listdir('cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f"cogs.{file[:-3]}")


async def main():
    await load_cogs()
    await bot.start(config['token'])

if __name__ == '__main__':
    asyncio.run(main())

