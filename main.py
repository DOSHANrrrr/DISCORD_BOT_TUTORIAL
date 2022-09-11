import discord
import json
import qrcode
from discord.ext import commands
import os

file = open('config.json', 'r')
config = json.load(file)

bot = commands.Bot(config['prefix'])

@bot.event
async def on_ready():
    print('BOT ONLINE')

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'{ctx.author.mention} pong!')

@bot.command(name='foo')
async def ping(ctx: commands.context, *, args):
    result = str(args)
    await ctx.send(embed=discord.Embed(title=f'{result}', description="Hi, this is a test command" , color=0x64ff0a))

@bot.command(name='qr')
async def make_qr_code(ctx, *, args):
    file_name = str(args).replace(' ', '_')

    img = qrcode.make(file_name + '.png')

    try:
        img.save(file_name + '.png')
    except:
        print(1)

    await ctx.send(file=discord.File(os.path.abspath(file_name + '.png')))

    os.remove(os.path.abspath(file_name + '.png'))

bot.run(config['token'])
