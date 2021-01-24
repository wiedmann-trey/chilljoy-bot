import yaml
import random

with open("config.yaml", 'r') as stream:
    bot_config = yaml.safe_load(stream)

@bot.command(name='brightness')
async def brightness(ctx):
    await ctx.send(bot_config["brightness"]["text"])
    await ctx.send(file=discord.File(bot_config["brightness"]["image"]))

@bot.command(name='posture')
async def posture(ctx):
    await ctx.send(bot_config["posture"]["text"])
    await ctx.send(file=discord.File(bot_config["posture"]["image"]))

@bot.command(name='wrist')
async def wrist(ctx):
    exercises = bot_config["wrist"]["exercises"]
    r = random.randrange(len(exercises))
    await ctx.send(bot_config["wrist"]["text"])
    await ctx.send(exercises[r]["text"])
    await ctx.send(file=discord.File(exercises[r]["image"]))