import os
import pymongo
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

dbname = 'test'
password = os.getenv('DATA_PASSWORD')

client = pymongo.MongoClient(f'mongodb+srv://admin:{password}@cluster0.hitjj.mongodb.net/{dbname}?retryWrites=true&w=majority')
db = client['test']
db.test1.insert_one({"trey": "is cool"})

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.presences = True

bot = commands.Bot(command_prefix='g!', intents=intents)



async def check_game(ctx):
    while True:
        for guild in bot.guilds:
            for m in guild.members:
                for a in m.activities:
                    if a.type == discord.ActivityType.playing:
                        await ctx.send(f'{m.name} is playing {a.name}')
        await asyncio.sleep(30)


async def send_dms():
    for guild in bot.guilds:
        for m in guild.members:
            if m.bot == True:
                continue
            playing = False
            print(f'{m.name} dm: {m.dm_channel}')
            if m.dm_channel == None:
                print("hi")
                await m.create_dm()

            for a in m.activities:
                if a.type == discord.ActivityType.playing:
                    playing = True
                    await m.dm_channel.send(f'You are playing {a.name}')

            if not(playing):
                await m.dm_channel.send(f'You are not playing a game')

        

# @client.event
# async def on_ready():
#     guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    
#     print(f'{client.user} is connected to the following guild:\n'
#             f'{guild.name}(id: {guild.id})')

# @client.event
# async def on_member_join(member):
#     print('HI')
#     print(f'{member.display_name}')
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     await message.channel.send(f'YOU SUCK {message.author.name}')


@bot.command(name='hi')
async def hi(ctx):
    await ctx.send("YOU ARE COOL!")

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
    
#     await message.channel.send(f'YOU SUCK {message.author.name}')

@bot.command(name='join')
async def join(ctx):
    member = ctx.author
    print(member)


@bot.command(name='population')
async def population(ctx):
    for guild in bot.guilds:
        for member in guild.members:
            await ctx.send(member)

@bot.command(name='game')
async def game(ctx):
    await send_dms()
    await check_game(ctx)
    
    
    


bot.run(TOKEN)