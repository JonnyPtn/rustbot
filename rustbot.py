
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import logging
import os
from os.path import exists
import re

logging.basicConfig(level=logging.INFO)

bot = commands.bot.Bot('!')
last_rust_mention = datetime.now()

prog = re.compile(r"\b(?<!!)rust\b", re.IGNORECASE)

@bot.command()
async def rust(ctx):
    with open("last_mention", 'r') as file:
        last_mention = datetime.strptime(file.read(), "%d-%b-%Y (%H:%M:%S.%f)")
    since = datetime.now() - last_mention
    hours = since.seconds // 3600
    minutes = since.seconds // 60
    if since.days >= 1:
        message = f"It's been {since.days} day{'s' if since.days > 1 else ''} since rust was mentioned"
    elif hours >= 1:
        message = f"It's been {hours} hour{'s' if hours > 1 else ''} since rust was mentioned"
    elif minutes >= 1:
        message = f"It's been {minutes} minute{'s' if minutes > 1 else ''} since rust was mentioned"
    else:
        message = f"It's been {since.seconds} second{'s' if since.seconds > 1 else ''} since rust was mentioned"

    await ctx.send(message)

@bot.command()
async def record(ctx):
    with open("record", 'r+') as file:
        record_seconds = int(file.read())
        days = record_seconds // (3600 * 24)
        hours = record_seconds // 3600
        minutes = record_seconds // 60
        if days >= 1:
            await ctx.send(f"The longest time without mentioning rust is {days} day{'s' if days > 1 else ''}")
        if hours >= 1:
            await ctx.send(f"The longest time without mentioning rust is {hours} hour{'s' if hours > 1 else ''}")
        elif minutes >= 1:
            await ctx.send(f"The longest time without mentioning rust is {minutes} minute{'s' if minutes > 1 else ''}")
        else:
            await ctx.send(f"The longest time without mentioning rust is {record_seconds} second{'s' if record_seconds > 1 else ''}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    result = prog.search(message.content)
    if result is not None:
        if exists("last_mention"):
            with open("last_mention", 'r+') as file:
                last_mention = datetime.strptime(file.read(), "%d-%b-%Y (%H:%M:%S.%f)")

            since = datetime.now() - last_mention
            with open("record", 'r+') as file:
                record_seconds = int(file.read())
                if since.seconds > record_seconds:
                    hours = since.seconds // 3600
                    minutes = since.seconds // 60
                    if hours >= 1:
                        await message.channel.send(f"You lasted over {hours} hour{'s' if hours > 1 else ''} since mentioning rust, that's a new record!")
                    elif minutes >= 1:
                        await message.channel.send(f"You lasted over {minutes} minute{'s' if minutes > 1 else ''} since mentioning rust, that's a new record!")
                    else:
                        await message.channel.send(f"You lasted over {since.seconds} second{'s' if since.seconds > 1 else ''} since mentioning rust, that's a new record!")
                    file.seek(0)
                    file.write(str(since.seconds))
                    file.truncate()

        with open('last_mention', 'w') as file:
            file.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))

    await bot.process_commands(message)

load_dotenv()
bot.run(os.getenv('DISCORD_KEY'))