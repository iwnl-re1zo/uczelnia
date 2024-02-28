#!/usr/bin/env python3

import discord
from discord.ext import commands
import sqlite3 as sq
from top_secret import TOKEN

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=':', intents=intents)
token = TOKEN
valid_users = ["444941100466176000"] #discord id -> iwnl-re1zo (admin)
error_message = "**You are not authorized to use this command or try change the target channel**"
database_path = r'/Users/iwnl-re1zo/Documents/dev/python/studia/bot-hosting/backend/database/web-bots.db'


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="trying to have some fun :/"))
    print("NekoGirl testing new toys")
    pass

@bot.command()
async def members(message : discord.Message):
    
    con = sq.connect(database_path)
    cur = con.cursor()
    database_dcAdmins_table = [i for i in cur.execute(f'SELECT id_dc FROM dc_admins') for i in i]
    if message.author.id in database_dcAdmins_table or str(message.author.id) in valid_users:
        server = bot.guilds[0]
        for member in server.members:
            id_dc = member.id
            nick_dc = member.name
            if not member.bot:
                cur.execute(f'INSERT INTO discord_members (id_dc, nick_dc) VALUES(?,?)', (id_dc, nick_dc))
    else:
        await message.channel.send(error_message)
        
    con.commit()
    con.close()

@bot.command()
async def admins(message : discord.Message):

    con = sq.connect(database_path)
    cur = con.cursor()
    database_dcAdmins_table = [i for i in cur.execute(f'SELECT id_dc FROM dc_admins') for i in i]
    if message.author.id in database_dcAdmins_table or str(message.author.id) in valid_users:
        server = bot.get_guild(1071420377131130921)
        role = discord.utils.get(server.roles, id=1071421270236864672)
        members = [member for member in server.members if role in member.roles]
        for member in members:
            if not member.bot:
                cur.execute(f'INSERT INTO dc_admins (id_dc, nick_dc) VALUES(?,?)', (member.id, member.name))
    else:
        await message.channel.send(error_message)
    
    con.commit()
    con.close()

@bot.command()
async def register(message : discord.Message, *words):
    
    con = sq.connect(database_path)
    cur = con.cursor()
    database_dcAdmins_check_table = [i for i in cur.execute(f'SELECT id_dc FROM dc_admins') for i in i]
    if message.author.id in database_dcAdmins_check_table:
        iddc = message.author.id
        dc_nick = message.author.name
        nrtel = words[0]
        firstname = words[1]
        secondname = words[2]
    
        database_dcAdmins_table = [i for i in cur.execute(f'SELECT id_dc FROM dc_admins') for i in i]
        database_dcAdmin_table = [i for i in cur.execute(f'SELECT id_dc FROM admin') for i in i]

        if message.author.id in database_dcAdmins_table and message.author.id in database_dcAdmin_table:
         await message.channel.send(f'**User: {message.author.name} already exist in database**')
        elif message.author.id in database_dcAdmins_table and message.author.id not in database_dcAdmin_table:
            cur.execute(f'INSERT INTO admin (id_dc, nick_dc, nr_tel, first_name, second_name) VALUES(?,?,?,?,?)', (iddc, dc_nick, nrtel, firstname, secondname))
            await message.channel.send(f'**User: {message.author.name} registered successful**')

        con.commit()
        con.close()
    else:
        await message.channel.send(error_message)

bot.run(token)