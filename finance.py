from os import name
from typing import DefaultDict
from aiohttp.client import request
from asyncio.tasks import sleep
import discord
from discord import member
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime
import random
import requests
from bs4 import BeautifulSoup
import asyncio
import json
import time
from neispy import Neispy
import re
import PingPongWr

url = "https://builder.pingpong.us/api/builder/60447496e4b078d873a201b5/integration/v0.2/custom/{sessionId}"
pingpong_token = "Basic a2V5OjdkZWRiZGZiNTdkNDNmNGI0MWUyOGZmMjY5ZmQzMThk"
Ping = PingPongWr.Connect(url, pingpong_token)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# @tasks.loop(seconds=1)
# async def second():
#     now = datetime.now()
#     channel = bot.get_channel(1037312476620013648)
#     if now.minute == 19 and now.second == 1:
#         await channel.send("수업 2분전")
#     time.sleep(1)

weekday = ['월', '화', '수', '목', '금']

@bot.event
async def on_ready():
    print(bot.user.id)
    print("Success")
    # second.start()

@bot.command(aliases=['vmap','valorantmap','발로란트맵','발맵'])
async def test_(ctx, *, execpt='None'):
    execpt = execpt.split(" ")
    valorantMaps = ['펄','프랙처','브리즈','아이스박스','바인드','헤이븐','스플릿','어센트']

    for i in execpt:
        if i in valorantMaps:
            valorantMaps.remove(i)
    await ctx.reply("맵: **{}** | `후보: {}`".format(random.choice(valorantMaps), valorantMaps))



@bot.command(aliases=['급식'])
async def lunch_(ctx, current_day = time.strftime('%Y%m%d', time.localtime(time.time()))):
    # if current_day 공휴일에 입력시 가능한 다음날로 출력
    async with Neispy() as neis:
        scinfo = await neis.schoolInfo(SCHUL_NM="서울금융고등학교")
        ae = scinfo[0].ATPT_OFCDC_SC_CODE  # 교육청 코드
        se = scinfo[0].SD_SCHUL_CODE  # 학교 코드
        scmeal = await neis.mealServiceDietInfo(ae, se, MLSV_YMD=str(current_day))
    meal = scmeal[0].DDISH_NM.replace("<br/>", "\n")
    result = re.compile('[가-힣]+').findall(meal)
    result = "\n".join(result)
    now = datetime.now()
    await ctx.reply("{}년 {}월 {}일 ({}요일) 급식입니다.\n```\n{}\n```".format(now.year, now.month, now.day, weekday[now.weekday()], result))

@bot.command(aliases=['학사일정'])
async def schedule_(ctx, current_day = time.strftime('%Y%m%d', time.localtime(time.time()))):
    async with Neispy() as neis:
        scinfo = await neis.schoolInfo(SCHUL_NM="서울금융고등학교")
        ae = scinfo[0].ATPT_OFCDC_SC_CODE  # 교육청 코드
        se = scinfo[0].SD_SCHUL_CODE  # 학교 코드
        scschedule = await neis.SchoolSchedule(ae, se, AA_YMD=str(current_day))
        schedule = scschedule[0].EVENT_NM
    await ctx.reply("```\n{}\n```".format(schedule))   

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1036294870354116658)
    await member.edit(nick = '외부인님 채팅 확인해 주세요')
    await channel.send("{}님 안녕하세요! 이 채널에 `이름, 학년(나이)` 적어주세요.".format(member.mention))

@bot.command(name='sayd')
async def sayd_(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(msg)

@bot.command(aliases=['도움말'])
async def help_(ctx):
    await ctx.reply("**vmap**\n> !vmap [제외할맵]\n> ex) '!vmap 펄 브리즈'\n\n**급식**\n> !급식 [날짜]\n> ex) '!급식 221103'\n\n**학사일정**\n> !학사일정 [날짜]\n> ex) '!학사일정 221103'\n\n" + "[선택항목], <필수항목>")

with open('token.txt', 'r') as f:
    token = f.readline()

@bot.command(name='!')
async def aitalk(ctx, *, msg):
    if ctx.author == bot.user:
        return
    return_data = await Ping.Pong(session_id ="None", text = msg, topic = True, image = True, dialog = True) # 핑퐁빌더 API에 Post 요청
    await ctx.reply(f"{return_data['text']}")

@bot.event
async def on_message(msg = '안녕'):

    if msg.author == bot.user:
            await bot.process_commands(msg)
            return

    if msg.content.startswith("금융아 "):
        str_text = "".join((msg.content.split(" "))[1:])
        return_data = await Ping.Pong(session_id =str(msg.author.id) , text = str_text, topic = True, image = True, dialog = True) # 핑퐁빌더 API에 Post 요청
        await msg.reply(f"{return_data['text']}")
        await bot.process_commands(msg)

    await bot.process_commands(msg)

@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")

#leave cmd
@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")

bot.run(token)