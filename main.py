import discord
import json
from discord.ext import commands

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

bot.run(config['token'])
