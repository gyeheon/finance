from os import name
from typing import DefaultDict
from aiohttp.client import request
from asyncio.tasks import sleep
import discord
from discord import member
from discord.ext import commands
from discord.utils import get
import datetime
import random
import requests
from bs4 import BeautifulSoup
import asyncio
import json
import time
from neispy import Neispy
from asyncio.events import get_event_loop


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(bot.user.id)
    print("Success")
      


@bot.command(aliases=['vmap','valorantmap','발로란트맵','발맵'])
async def test_(ctx, *, execpt='None'):
    execpt = execpt.split(" ")
    valorantMaps = ['펄','프랙처','브리즈','아이스박스','바인드','헤이븐','스플릿','어센트']

    for i in execpt:
        if i in valorantMaps:
            valorantMaps.remove(i)
    await ctx.reply("맵: **{}** | `후보: {}`".format(random.choice(valorantMaps), valorantMaps))

@bot.command(aliases=['도움말'])
async def help_(ctx):
    await ctx.reply("**vmap**\n> !vmap [제외할맵]\n> ex) '!vmap 펄 브리즈' ")

@bot.command(aliases=['급식'])
async def lunch_(ctx):
    async with Neispy() as neis:
        scinfo = await neis.schoolInfo(SCHUL_NM="서울금융고등학교")
        AE = scinfo[0].ATPT_OFCDC_SC_CODE  # 교육청 코드
        SE = scinfo[0].SD_SCHUL_CODE  # 학교 코드
        current_day = time.strftime('%Y%m%d', time.localtime(time.time()))
        scmeal = await neis.mealServiceDietInfo(AE, SE, MLSV_YMD=str(current_day))
        meal = scmeal[0].DDISH_NM.replace("<br/>", "\n")
    await ctx.reply("```\n{}\n```".format(meal))


with open('token.txt', 'r') as f:
    token = f.readline()    

bot.run(token)