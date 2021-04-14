import json
import discord
from discord.ext import commands
import functools
import itertools
import math
import random
import asyncio
import youtube_dl
from async_timeout import timeout
import discapty
import textcaptcha
import aioconsole
from discord.utils import get
import random
import datetime
import time








bot = commands.Bot(command_prefix='$')

game = discord.Game("Doing Stuff")


bot.remove_command('help')

    

    
        
    
    




@bot.command(pass_context=True)

async def verify(ctx):
    def check(message):
        
        return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)
    
    fetcher = textcaptcha.CaptchaFetcher()
    captcha = fetcher.fetch()
    
    yes = discord.Embed(title="Question", description=captcha.question, color=0x72d345)
    await ctx.author.send(embed=yes)
    

    await ctx.send("Sent A DM")
    try:
        answer = await bot.wait_for("message",check=check,timeout=30)
        
    except asyncio.TimeoutError:
        await ctx.author.send("Sorry, you didn't reply in time!")
    
    
    response = (answer.content)
    member = ctx.author
    role = discord.utils.get(member.guild.roles, name="Verified")

    if captcha.check_answer(response):
        await ctx.author.send("Now a Verified Member")
        await member.add_roles(role)
        channel = bot.get_channel(828740756755447838)

        await channel.send(ctx.author.mention+" is now verified")
    else:
        await ctx.author.send("You're a Robot")


@bot.command()
async def nuke(ctx, channel: discord.TextChannel = None):
    if channel == None: 
        await ctx.send("You did not mention a channel!")
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        new_channel = await nuke_channel.clone(reason="Has been Nuked!")
        await nuke_channel.delete()
        await new_channel.send("THIS CHANNEL HAS BEEN NUKED!")
        await ctx.send("Nuked the Channel sucessfully!")

    else:
        await ctx.send(f"No channel named {channel.name} was found!")


@bot.event
async def on_ready():
    print('Bot online')
    global users
    try:
        with open('ranking.json') as f:
            users = json.load(f)
            sort = sorted(users, key=lambda x : users[x].get('experience', 0), reverse=True)
            print(sort)


    except FileNotFoundError:
        print("norank.json")
        users = {}

@bot.command()
async def coins(ctx):
        id_user = str(ctx.author.id)
        
        coins= users[id_user]["coin"]
        coin = discord.Embed(color=0xFF0000)

        coin.add_field(name="Coins", value=coins, inline=False)
        coin.timestamp = datetime.datetime.utcnow()

    
        await ctx.send(embed=coin)


        
           










@bot.event
async def on_message(message):
    id_user = str(message.author.id)
    if message.author == bot.user:
        return
    xp = random.randrange(5, 10)
    if id_user not in users:
        print(message.author.name)
        users[id_user] = {}
        users[id_user]["experience"] = 0
        users[id_user]["level"] = 0
        users[id_user]["coin"] = 0

    users[id_user]["experience"] += xp
    
    experience = users[id_user]["experience"]
    lvl_start = users[id_user]["level"]
    lvl_end = int(experience ** (1 / 4))
    coin_start = users[id_user]["coin"] 
    coin_end = int(experience ** (1 /5))
    if lvl_start < lvl_end:
        await message.channel.send(f"{message.author.mention} has risen to the level {lvl_end}")
        users[id_user]["level"] = lvl_end

    if coin_start < coin_end:
        await message.channel.send(f"{message.author.mention} has now {coin_end} coins")
        users[id_user]["coin"] = coin_end
        
        
    _save()
    await bot.process_commands(message)

    
    
    bad_words = ["fuck","bitch","cunt"]

    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            print("A bad word was said")
            
    


def _save():
    with open('ranking.json', 'w+') as f:
        json.dump(users, f)

@bot.command()
async def help(ctx):
        embed = discord.Embed(title="Help", description="Some useful commands")
        embed.add_field(name="$stats", value="Shows User Stats")
        embed.add_field(name="$leaderboard", value="Shows server leaderboard")
        embed.add_field(name="$dice", value="Lets the user roll a dice")

        await ctx.send(content=None, embed=embed)

@bot.command()
async def stats(ctx):

        id_user = str(ctx.author.id)

        lvl = users[id_user]["level"]
        
        coins = users[id_user]["coin"] 
        
        experience =  users[id_user]["experience"]
        
        who = discord.Embed(title="Stats")
        who.add_field(name="Username", value=ctx.author, inline=False)

        who.add_field(name="Level", value=lvl, inline=False)
        who.add_field(name="XP", value=experience, inline=False)
        who.add_field(name="Coins:", value=coins, inline=False)
        who.timestamp = datetime.datetime.utcnow()
        who.set_thumbnail(url=ctx.author.avatar_url)


        await ctx.send(embed=who)




@bot.command()

async def leaderboard(ctx):

    with open('ranking.json', 'r') as f:
        data = json.load(f)

    top_users = {k: v for k, v in sorted(data.items(), key=lambda item: item[1]["experience"], reverse=True)}

    names = ''
    for postion, user in enumerate(top_users):
        names += f"{postion+1}.<@!{user}> \n  {top_users[user]['experience']} points\n\n"

    embed = discord.Embed(title="Leaderboard")
    embed.add_field(name="Names", value=names, inline=False)
    embed.timestamp = datetime.datetime.utcnow()

    
    await ctx.send(embed=embed)


@bot.command()
async def dice(ctx):
    message = await ctx.send("Choose a number:\n**4**, **6**, **8**, **10**, **12**, **20** ")
    
    def check(m):
        return m.author == ctx.author

    try:
        message = await bot.wait_for("message", check = check, timeout = 30.0)
        m = message.content

        if m != "4" and m != "6" and m != "8" and m != "10" and m != "12" and m != "20":
            await ctx.send("Sorry, invalid choice.")
            return
        
        coming = await ctx.send("Here it comes...")
        time.sleep(1)
        await coming.delete()
        await ctx.send(f"**{random.randint(1, int(m))}**")
    except asyncio.TimeoutError:
        await message.delete()
        await ctx.send("Procces has been canceled because you didn't respond in **30** seconds.")






@bot.command()
async def give(ctx, *, user: discord.User):
    id_user = str(ctx.author.id)
    coins = users[id_user]["coin"] 
    amount = 1

    if user:
        await ctx.send(f"gave one coin to, {user.mention}")
        
        id_user = str(user.id)
        users[id_user]["coin"] += amount
        
        id_user = str(ctx.author.id)
        users[id_user]["coin"] -= amount
    else:
        await ctx.send('You have to mention who you what to give a coin to')
        
        








@bot.command()
async def work(ctx):
    id_user = str(ctx.author.id)
    amount = random.randrange(1, 10)
    users[id_user]["coin"] += amount
    await ctx.send(f"{ctx.author.mention} was given {amount} coin by working")











    






bot.run('ODMxOTk1OTkzMTEzMzYyNDgy.YHdWpg.zq2mhMYzOUTt59RiNb1mfP78wLs')

