import os
import pymongo
import asyncio
import pickle
import datetime

from timer import Scheduler

from tasks import TaskScheduler

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

dbname = 'chilljoy-bot'
password = os.getenv('DATA_PASSWORD')

client = pymongo.MongoClient(f'mongodb+srv://admin:{password}@cluster0.hitjj.mongodb.net/{dbname}?retryWrites=true&w=majority')
db = client['chilljoy-bot']

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.presences = True

bot = commands.Bot(command_prefix='g!', intents=intents)

timer_schedule = Scheduler(1)

def find_user(idd):
    for guild in bot.guilds:
        for m in guild.members:
            if m.id == idd:
                return m

async def send_20_min(user):
    print("20 min achieved")
    m = find_user(user)

    data = db.users.find_one({"id": m.id})

    if m.dm_channel == None:
        await m.create_dm()

    if data["currently_playing"] == True:
        tips = bot_config["health_reminders"]["tips"]
        r = random.randrange(len(tips)
        await m.dm_channel.send("Reminder:")
        await m.dm_channel.send(tips[r])
    
    db.users.update_one({"id": m.id}, {'$set': {"20_min_reminder": False}})

async def send_1_hr(user):
    print("1 hr achieved")
    m = find_user(user)

    data = db.users.find_one({"id": m.id})

    if m.dm_channel == None:
        await m.create_dm()

    if data["currently_playing"] == True:
        await m.dm_channel.send(bot_config["health_reminders"]["hourly"])
    
    db.users.update_one({"id": m.id}, {'$set': {"1_hr_reminder": False}})

async def check_game(channel):
    while True:
        for guild in bot.guilds:
            for m in guild.members:
                exist = db.users.find_one({"id": m.id})
                if exist != None:
                    playing = False
                    for a in m.activities:
                        if a.type == discord.ActivityType.playing:
                            playing = True
                            await channel.send(f'{m.name} is playing {a.name}')
                    
                    if exist["currently_playing"] != playing:
                        db.users.update_one({"id": m.id}, {'$set': {"currently_playing": playing}})
        await asyncio.sleep(10)

async def set_timers():
    while True:
        for guild in bot.guilds:
            for m in guild.members:
                exist = db.users.find_one({"id": m.id})
                if exist != None:
                    if exist['currently_playing'] == True:
                        if exist['20_min_reminder'] == False and exist['health_reminders']==True:
                            timer_schedule.addEvent(datetime.timedelta(minutes=20), m.id, send_20_min)
                            db.users.update_one({"id": m.id}, {'$set': {"20_min_reminder": True}})
                        if exist['1_hr_reminder'] == False and exist['health_reminders']==True:
                            timer_schedule.addEvent(datetime.timedelta(hours=1), m.id, send_1_hr)
                            db.users.update_one({"id": m.id}, {'$set': {"1_hr_reminder": True}})
        
        await asyncio.sleep(10)

async def check_tasks():
    while True:
        for guild in bot.guilds:
            for m in guild.members:
                exist = db.users.find_one({"id": m.id})
                if exist != None:
                    a=exist

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

        

@bot.event
async def on_ready():
    for guild in bot.guilds:
        for m in guild.members:
            exist = db.users.find_one({"id": m.id})
            if exist != None:
                db.users.update_one({"id": m.id}, {'$set': {
                    "currently_playing": False,
                    "task_reminders": False,
                    "health_reminders": False,
                    "20_min_reminder": False,
                    "1_hr_reminder": False}})
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    
    print(f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})')

    print(guild.channels)

    chan=0

    for channel in guild.channels:
        if channel.name == "playing":
            chan = channel



    await asyncio.gather(
        check_game(chan),
        set_timers(),
        timer_schedule.loop()
    )

    # print("hi")

    # await set_timers()

    # loop = asyncio.create_task(timer_schedule.loop)
    # # sched.addEvent(time, user, func)
    # # loop = asyncio.create_task(sched.loop)

    # await loop

    

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

@bot.command(name='join')
async def join(ctx):
    member = ctx.author
    exist = db.users.find_one({"id": member.id})
    if exist == None:
        await ctx.send(f'Hi {member.name}! We are adding you to our list of users.')
        sched = TaskScheduler()
        store = pickle.dumps(sched)
        db.users.insert_one({
            "id": member.id,
            "name": member.name,
            "currently_playing": False,
            "task_reminders": False,
            "health_reminders": False,
            "20_min_reminder": False,
            "1_hr_reminder": False,
            "task_scheduler": store
            })
    else:
        await ctx.send(f'{member.name} is already a user!')

@bot.command(name='task')
async def task(ctx, *args):
    m = ctx.author
    exist = db.users.find_one({"id": m.id})
    
    if exist == None:
        await ctx.send("You aren't on our list of users. Type 'g!join' if you want to be added!")
        return
    if len(args) == 0:
        await ctx.send("That was not an acceptable argument. Try typing 'on' or 'off' after 'g!task'")
        return
    arg = args[0]

    inpt = arg.strip()
    if inpt == 'on':
        db.users.update_one({"id": m.id}, {'$set': {"task_reminders": True}})
        await ctx.send("Your task reminders have been turned on!")
    elif inpt == 'off':
        db.users.update_one({"id": m.id}, {'$set': {"task_reminders": False}})
        await ctx.send("Your task reminders have been turned off!")
    else:
        await ctx.send("That was not an acceptable argument. Try typing 'on' or 'off' after 'g!task'")

@bot.command(name='health')
async def health(ctx, *args):
    
    m = ctx.author
    exist = db.users.find_one({"id": m.id})

    if exist == None:
        await ctx.send("You aren't on our list of users. Type 'g!join' if you want to be added!")
        return
    if len(args) == 0:
        await ctx.send("That was not an acceptable argument. Try typing 'on' or 'off' after 'g!health'")
        return
    arg = args[0]

    inpt = arg.strip()
    if inpt == 'on':
        db.users.update_one({"id": m.id}, {'$set': {"health_reminders": True}})
        await ctx.send("Your health reminders have been turned on!")
    elif inpt == 'off':
        db.users.update_one({"id": m.id}, {'$set': {"health_reminders": False}})
        await ctx.send("Your health reminders have been turned off!")
    else:
        await ctx.send("That was not an acceptable argument. Try typing 'on' or 'off' after 'g!health'")
        
    
        

@bot.command(name='addtask')
async def addtask(ctx, *args):
    m = ctx.author
    exist = db.users.find_one({"id": m.id})
    
    if exist == None:
        await ctx.send("You aren't on our list of users. Type 'g!join' if you want to be added!")
        return

    hi = pickle.loads(exist["task_scheduler"])
    print(hi)

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


