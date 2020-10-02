import asyncio
from urllib.request import urlopen
import discord
from urllib.request import Request
import urllib
import bs4
from urllib import parse

import pytz as pytz
from bs4 import BeautifulSoup
import datetime
from bs4 import BeautifulSoup
import random
import fmt
import time
from selenium import webdriver
import os
from urllib.parse import quote
import re
from urllib.request import Request, urlopen
from discord.ext import commands
import warnings
import json
import unicodedata
import urllib.request
from urllib.request import URLError
from urllib.request import HTTPError
import requests
from tqdm import tqdm

from selenium.webdriver.chrome import webdriver

operatoriconURLDict = dict()

countG = 0
client = discord.Client()
players = {}
queues= {}
musiclist=[]
mCount=1
searchYoutube={}
searchYoutubeHref={}



tierScore = {
    'default' : 0,
    'iron' : 1,
    'bronze' : 2,
    'silver' : 3,
    'gold' : 4,
    'platinum' : 5,
    'diamond' : 6,
    'master' : 7,
    'grandmaster' : 8,
    'challenger' : 9
}
def tierCompare(solorank,flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2
warnings.filterwarnings(action='ignore')
bot = commands.Bot(command_prefix='마고야')

opggsummonersearch = 'https://www.op.gg/summoner/userName='


def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>','',str(htmls[a]),0).strip()
    return htmls

client_id = "BE04xPQVZCSF63CKYMSd"
client_secret = "6qdPyMTkJa"

def check_queue(id):
    if queues[id]!=[]:
        player = queues[id].pop(0)
        players[id] = player
        del musiclist[0]
        player.start()

        def deleteTags(htmls):
            for a in range(len(htmls)):
                htmls[a] = re.sub('<.+?>', '', str(htmls[a]), 0).strip()
            return htmls

        entData = quote("")
        dataParmas = "source=en&target=id&text=" + entData
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"

        request = Request(baseurl)

        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urlopen(request, data=dataParmas.encode("utf-8"))
        responsedCode = response.getcode()
        if (responsedCode == 200):
            response_body = response.read()

            api_callResult = response_body.decode('utf-8')
            stringConvertJSON = api_callResult.replace("'", "\"")
            api_callResult = json.loads(stringConvertJSON)
            translatedText = api_callResult['message']['result']["translatedText"]
            print(translatedText)
        else:
            print("Error Code : " + responsedCode)


        unisoftURL = "https://www.ubisoft.com"
        rainbowSixSiegeOperatorIconURL = "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/game-info/operators"
        html = requests.get(rainbowSixSiegeOperatorIconURL).text
        bs = BeautifulSoup(html, 'html.parser')

        operatorListDiv = bs.findAll('div', {'ccid': re.compile('[0-9A-Za-z]*')})
        print("Initiating Rainbow Six Siege Operators' Information....")
        for ind in tqdm(range(0, len(operatorListDiv))):
            operatormainURL = operatorListDiv[ind].a['href']

            operatorname = operatormainURL.split('/')[-1]

            html2 = requests.get(unisoftURL + operatormainURL).text
            bs2 = BeautifulSoup(html2, 'html.parser')
            operatoriconURL = bs2.find('div', {'class': "operator__header__icons__names"}).img['src']
            operatoriconURLDict[operatorname] = operatoriconURL



        



client = discord.Client()

r6URL = "https://r6.op.gg/"
playerSite = 'https://opgg-gnb.akamaized.net/index.js?t=1601371241'


def convertToNormalEnglish(text):
    return ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')

calcResult = 0

@client.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(client.user.name)
    print(client.user.id)
    print("==========")

    async def bt(games):
        await client.wait_until_ready()
        guild_list = client.guilds

        while not client.is_closed():
            for g in games:
                await client.change_presence(status=discord.Status.online, activity=discord.Game(g))
                await asyncio.sleep(5)
    await bt(['마고야 도움말','2020-09-03출생','아직 미완성'])


@client.event
async def on_message(message):
    if message.content.startswith("마고야 안녕"):
        await message.channel.send("응 안녕")
    if message.content == "마고야 도움말":
        embed = discord.Embed(title="도움말", description='''마고의 명령어 입니다''', color=0x8285FA)
        embed.add_field(name="대화", value="뭐해/갠디/마마고(마고야 x)", inline=False)
        embed.add_field(name="놀이", value="사다리타기 (사람/결과)/가위바위보/주사위/타이머", inline=False)
        embed.add_field(name="전적검색", value="메이플 (닉네임)/경쟁전(1.2)배그솔로(1,2)듀오(1,2)스쿼드(1,2) (닉네임)\n롤전적 (닉네임)", inline=False)
        embed.add_field(name="잡다한 기능 ", value="1부터10/시간/핑/골라(목록)/사진 (원하는것)/번역 (내용)\n음식추천/계산 (더하기,빼기,곱하기,나누기) 숫자 숫자/정보/날씨\n이모티콘", inline=False)
        embed.add_field(name="특수기능", value="식제 메시지 감지/새로온 유저 감지/코로나/메시지 수정 감지", inline=False)
        embed.add_field(name="봇 초대하기", value="[바로가기](https://discord.com/oauth2/authorize?client_id=734049531548794880&scope=bot)", inline=False)
        embed.add_field(name="이것은 필드입니다.", value="필드의 값입니다.", inline=False)
        embed.set_footer(text="추가할거 추천받습니다",icon_url="https://cdn.discordapp.com/attachments/743810244982866093/761510874120060948/ea5324eab314050c.jpg")
        await message.channel.send(embed=embed)
    if message.content.startswith("마고야 뭐해"):
        what = "니생각 롤 밥먹어 아무것도 배그 옵치 레식 멍때리기 알면서ㅎ 여친생각 공부 "
        whatchoice = what.split(" ")
        whatnumber = random.randint(2, len(whatchoice))
        whatresult = whatchoice[whatnumber]
        await message.channel.send(whatresult)
    if message.content.startswith("마고야 갠디"):
        await message.author.send("마고야 도움말 쳐봐 싫음 말고 ㅋ")
    if message.author.bot:
        return None
    if message.content.startswith("마마고"):
        await message.channel.send("응? 왜불러")
    if message.content.startswith("마고야 시간"):
        a = datetime.datetime.today().year
        b = datetime.datetime.today().month
        c = datetime.datetime.today().day
        d = datetime.datetime.today().hour
        e = datetime.datetime.today().minute
        await message.channel.send(str(a) + "년 " + str(b) + "월 " + str(c) + "일 " + str(d) + "시 " + str(e) + "분 이야")
    if message.content.startswith("마고야 핑"):
        embed=discord.Embed(title=':ping_pong:퐁!',description=str(round(client.latency*1000))+'ms',color=0x8285FA)
        await message.channel.send(embed=embed)
    if message.content.startswith("마고야 정보"):
        date = datetime.datetime.utcfromtimestamp(((int(message.author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(color=0x8285FA)
        embed.add_field(name="태그",value=message.author,inline=False)
        embed.add_field(name="서버 닉네임", value=message.author.display_name, inline=False)
        embed.add_field(name="가입일", value=str(date.year) + "년"+str(date.month) + "월"+str(date.day) + "일", inline=False)
        embed.add_field(name="아이디", value=message.author.id, inline=False)
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=embed)
    if message.content.startswith('마고야 이모티콘'):
        emoji = [" ꒰⑅ᵕ༚ᵕ꒱ ", " ꒰◍ˊ◡ˋ꒱ ", " ⁽⁽◝꒰ ˙ ꒳ ˙ ꒱◜⁾⁾ ", " ༼ つ ◕_◕ ༽つ ", " ⋌༼ •̀ ⌂ •́ ༽⋋ ",
                 " ( ･ิᴥ･ิ) ", " •ө• ", " ค^•ﻌ•^ค ", " つ╹㉦╹)つ ", " ◕ܫ◕ ", " ᶘ ͡°ᴥ͡°ᶅ ", " ( ؕؔʘ̥̥̥̥ ه ؔؕʘ̥̥̥̥ ) ",
                 " ( •́ ̯•̀ ) ",
                 " •̀.̫•́✧ ", " '͡•_'͡• ", " (΄◞ิ౪◟ิ‵) ", " ˵¯͒ བ¯͒˵ ", " ͡° ͜ʖ ͡° ", " ͡~ ͜ʖ ͡° ", " (づ｡◕‿‿◕｡)づ ",
                 " ´_ゝ` ", " ٩(͡◕_͡◕ ", " ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄ ", " ٩(͡ï_͡ï☂ ", " ௐ ", " (´･ʖ̫･`) ", " ε⌯(ง ˙ω˙)ว ",
                 " (っ˘ڡ˘ς) ", "●▅▇█▇▆▅▄▇", "╋╋◀", "︻╦̵̵̿╤──", "ー═┻┳︻▄", "︻╦̵̵͇̿̿̿̿══╤─",
                 " ጿ ኈ ቼ ዽ ጿ ኈ ቼ ዽ ጿ ", "∑◙█▇▆▅▄▃▂", " ♋♉♋ ", " (๑╹ω╹๑) ", " (╯°□°）╯︵ ┻━┻ ",
                 " (///▽///) ", " σ(oдolll) ", " 【o´ﾟ□ﾟ`o】 ", " ＼(^o^)／ ", " (◕‿‿◕｡) ", " ･ᴥ･ ", " ꈍ﹃ꈍ "
                                                                                                 " ˃̣̣̣̣̣̣︿˂̣̣̣̣̣̣ ",
                 " ( ◍•㉦•◍ ) ", " (｡ì_í｡) ", " (╭•̀ﮧ •́╮) ", " ଘ(੭*ˊᵕˋ)੭ ", " ´_ゝ` ", " (~˘▾˘)~ "]

        randomNum = random.randrange(0, len(emoji))
        print("랜덤수 값 :" + str(randomNum))
        print(emoji[randomNum])
        await message.channel.send(embed=discord.Embed(color=0x8285FA,description=emoji[randomNum]))
        await message.channel.send(embed=embed)

    if message.content.startswith("마고야 날씨"):
        learn = message.content.split(" ")
        location = learn[1]
        enc_location = urllib.parse.quote(location + '날씨')
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
        print(url)
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        todayBase = bsObj.find('div', {'class': 'main_info'})

        todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
        todayTemp = todayTemp1.text.strip()  # 온도
        print(todayTemp)

        todayValueBase = todayBase.find('ul', {'class': 'info_list'})
        todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
        todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
        print(todayValue)

        todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
        todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도
        print(todayFeelingTemp)

        todayMiseaMongi1 = bsObj.find('div', {'class': 'sub_info'})
        todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
        todayMiseaMongi3 = todayMiseaMongi2.find('dd')
        todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지
        print(todayMiseaMongi)

        tomorrowBase = bsObj.find('div', {'class': 'table_info weekly _weeklyWeather'})
        tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
        tomorrowTemp2 = tomorrowTemp1.find('dl')
        tomorrowTemp3 = tomorrowTemp2.find('dd')
        tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도
        print(tomorrowTemp)

        tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
        tomorrowMoring1 = tomorrowAreaBase.find('div', {'class': 'main_info morning_box'})
        tomorrowMoring2 = tomorrowMoring1.find('span', {'class': 'todaytemp'})
        tomorrowMoring = tomorrowMoring2.text.strip()  # 내일 오전 온도
        print(tomorrowMoring)

        tomorrowValue1 = tomorrowMoring1.find('div', {'class': 'info_data'})
        tomorrowValue = tomorrowValue1.text.strip()  # 내일 오전 날씨상태, 미세먼지 상태
        print(tomorrowValue)

        tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
        tomorrowAllFind = tomorrowAreaBase.find_all('div', {'class': 'main_info morning_box'})
        tomorrowAfter1 = tomorrowAllFind[1]
        tomorrowAfter2 = tomorrowAfter1.find('p', {'class': 'info_temperature'})
        tomorrowAfter3 = tomorrowAfter2.find('span', {'class': 'todaytemp'})
        tomorrowAfterTemp = tomorrowAfter3.text.strip()  # 내일 오후 온도
        print(tomorrowAfterTemp)

        tomorrowAfterValue1 = tomorrowAfter1.find('div', {'class': 'info_data'})
        tomorrowAfterValue = tomorrowAfterValue1.text.strip()

        print(tomorrowAfterValue)  # 내일 오후 날씨상태,미세먼지

        embed = discord.Embed(color=0x8285FA)
        embed.add_field(name='현재온도', value=todayTemp + '˚', inline=False)  # 현재온도
        embed.add_field(name='체감온도', value=todayFeelingTemp, inline=False)  # 체감온도
        embed.add_field(name='현재상태', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
        embed.add_field(name='현재 미세먼지 상태', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
        embed.add_field(name='오늘 오전/오후 날씨', value=tomorrowTemp, inline=False)  # 오늘날씨 # color=discord.Color.blue()
        embed.add_field(name='**----------------------------------**', value='**----------------------------------**',inline=False)  # 구분선
        embed.add_field(name='내일 오전온도', value=tomorrowMoring + '˚', inline=False)  # 내일오전날씨
        embed.add_field(name='내일 오전날씨상태, 미세먼지 상태', value=tomorrowValue, inline=False)  # 내일오전 날씨상태
        embed.add_field(name='내일 오후온도', value=tomorrowAfterTemp + '˚', inline=False)  # 내일오후날씨
        embed.add_field(name='내일 오후날씨상태, 미세먼지 상태', value=tomorrowAfterValue, inline=False)  # 내일오후 날씨상태

        await message.channel.send(embed=embed)

    if message.content.startswith('마고야 주사위'):

        randomNum = random.randrange(1, 7)
        print(randomNum)
        if randomNum == 1:
            await message.channel.send(embed=discord.Embed(description=':game_die: ' + ':one:'))
        if randomNum == 2:
            await message.channel.send(embed=discord.Embed(description=':game_die: ' + ':two:'))
        if randomNum == 3:
            await message.channel.send(embed=discord.Embed(description=':game_die: ' + ':three:'))
        if randomNum == 4:
            await message.channel.send(embed=discord.Embed(description=':game_die: ' + ':four:'))
        if randomNum == 5:
            await message.channel.send(embed=discord.Embed(description=':game_die: ' + ':five:'))
        if randomNum == 6:
            await message.channel.send(embed=discord.Embed(description=':game_die: ' + ':six: '))
    if message.content.startswith("마고야 사진"):
        Text = ""
        learn = message.content.split(" ")
        vrsize = len(learn)
        vrsize = int(vrsize)
        for i in range(1, vrsize):
            Text = Text + " " + learn[i]
        print(Text.strip())
        randomNum = random.randrange(0, 40)
        location = Text
        enc_location = urllib.parse.quote(location)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query=' + enc_location
        print(url)
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        imgfind1 = bsObj.find('div', {'class': 'photo_grid _box'})
        imgfind2 = imgfind1.findAll('a', {'class': 'thumb _thumb'})
        imgfind3 = imgfind2[randomNum]
        imgfind4 = imgfind3.find('img')
        imgsrc = imgfind4.get('data-source')
        print(imgsrc)
        embed = discord.Embed(color=0x8285FA)
        embed.set_image(url=imgsrc)
        await message.channel.send(embed=embed)
    if message.content.startswith("마고야 서버"):
        Cguilds = len(client.guilds)
        await message.channel.send(Cguilds)

    if message.content.startswith("마고야 사다리타기 "):
        team = message.content[10:]
        peopleteam = team.split("/")
        people = peopleteam[0]
        team = peopleteam[1]
        person = people.split(" ")
        teamname = team.split(" ")
        random.shuffle(teamname)
        for i in range(0,len(person)):
            await message.channel.send(person[i] + "은(는)" + teamname[i] + "입니다")
    if message.content.startswith("마고야 골라"):
        choice = message.content.split(" ")
        choicenumber = random.randint(2,len(choice)-1)
        choiceresult = choice[choicenumber]
        await message.channel.send(choiceresult)
    if message.content.startswith('마고야 가위바위보'):
        rsp = ["가위", "바위", "보"]
        embed = discord.Embed(title="가위바위보", description="가위바위보를 합니다 5초 내로 (가위/바위/보)를 써주세요!", color=0x8285FA)
        channel = message.channel
        msg1 = await message.channel.send(embed=embed)

        def check(m):
            return m.author == message.author and m.channel == channel

        try:
            msg2 = await client.wait_for('message', timeout=5.0, check=check)
        except asyncio.TimeoutError:
            await msg1.delete()
            embed = discord.Embed(title="가위바위보", description="앗 5초가 지났네요...!", color=0x8285FA)
            await message.channel.send(embed=embed)
            return
        else:
            await msg1.delete()
            bot_rsp = str(random.choice(rsp))
            user_rsp = str(msg2.content)
            answer = ""
            if bot_rsp == user_rsp:
                answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "아쉽지만 비겼습니다."
            elif (bot_rsp == "가위" and user_rsp == "바위") or (bot_rsp == "보" and user_rsp == "가위") or (
                    bot_rsp == "바위" and user_rsp == "보"):
                answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "아쉽지만 제가 졌습니다."
            elif (bot_rsp == "바위" and user_rsp == "가위") or (bot_rsp == "가위" and user_rsp == "보") or (
                    bot_rsp == "보" and user_rsp == "바위"):
                answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "제가 이겼습니다!"
            else:
                embed = discord.Embed(title="가위바위보", description="앗, 가위, 바위, 보 중에서만 내셔야죠...", color=0x8285FA)
                await message.channel.send(embed=embed)
                return
            embed = discord.Embed(title="가위바위보", description=answer, color=0x8285FA)
            await message.channel.send(embed=embed)
            return

    if message.content.startswith("마고야롤전적"):
        try:
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다!", description="", color=0x8285FA)
                embed.add_field(name="Summoner name not entered",
                                value="To use command 마고야롤전적 : 마고야롤전적 (Summoner Nickname)", inline=False)

                await message.channel.send("Error : Incorrect command usage ", embed=embed)
            else:
                playerNickname = ''.join((message.content).split(' ')[1:])
                # Open URL
                checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
                bs = BeautifulSoup(checkURLBool, 'html.parser')

                Medal = bs.find('div', {'class': 'SideContent'})
                RankMedal = Medal.findAll('img', {'src': re.compile(
                    '\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})

                mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})


                solorank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {'class': {'RankType', 'TierRank'}}))

                solorank_Point_and_winratio = deleteTags(
                    bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))

                flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {
                    'class': {'sub-tier__rank-type', 'sub-tier__rank-tier', 'sub-tier__league-point',
                              'sub-tier__gray-text'}}))

                flexrank_Point_and_winratio = deleteTags(bs.findAll('span', {'class': {'sub-tier__gray-text'}}))

                if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x8285FA)
                    embed.add_field(name="솔로 랭크 : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="자유 랭크 : Unranked", value="Unranked", inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])

                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)


                elif len(solorank_Point_and_winratio) == 0:


                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x8285FA)
                    embed.add_field(name="솔로 랭크 : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="자유 랭크", value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="모스트 챔피언 : " + mostUsedChampion,
                                    value="킬뎃 : " + mostUsedChampionKDA + " / " + " 승률 : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[1]['src'])

                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)


                elif len(flexrank_Point_and_winratio) == 0:


                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x8285FA)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name="솔로 랭크", value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name="자유 랭크 : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="모스트 챔피언 : " + mostUsedChampion,
                                    value="킬뎃 : " + mostUsedChampionKDA + " / " + "승률 : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])

                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)

                else:
                    solorankmedal = RankMedal[0]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')
                    flexrankmedal = RankMedal[1]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')


                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]


                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    cmpTier = tierCompare(solorankmedal[0], flexrankmedal[0])
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x8285FA)
                    embed.add_field(name="솔로 랭크", value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name="자유 랭크", value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="모스트 챔피언 : " + mostUsedChampion,
                                    value="킬뎃 : " + mostUsedChampionKDA + " / " + " 승률 : " + mostUsedChampionWinRate,
                                    inline=False)
                    if cmpTier == 0:
                        embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    elif cmpTier == 1:
                        embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    else:
                        if solorankmedal[1] > flexrankmedal[1]:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                        elif solorankmedal[1] < flexrankmedal[1]:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                        else:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])


                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="소환사 전적검색 실패", description="", color=0x8285FA)
            embed.add_field(name="", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
            await message.channel.send("Wrong Summoner Nickname")

        except UnicodeEncodeError as e:
            embed = discord.Embed(title="소환사 전적검색 실패", description="", color=0x8285FA)
            embed.add_field(name="???", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
            await message.channel.send("Wrong Summoner Nickname", embed=embed)

        except AttributeError as e:
            embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0x8285FA)
            embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)

            await message.channel.send("Error : Non existing Summoner ", embed=embed)

    if message.content.startswith("마고야경쟁전1"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)

        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x8285FA)
                embed.add_field(name="Player nickname not entered",
                                value="To use command 마고야경쟁전(1 : TPP or 2 : FPP) : 마고야경쟁전 (Nickname)", inline=False)

                await message.channel.send("Error : Incorrect command usage ", embed=embed)
            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                # Varaibel rankElements : index 0: fpp 1 : tpp

                rankElements = bs.findAll('div', {'class': re.compile('squad ranked [A-Za-z0-9]')})

                '''
                -> 클래스 값을 가져와서 판별하는 것도 있지만 이 방법을 사용해 본다.
                -> 만약 기록이 존재 하지 않는 경우 class 가 no_record라는 값을 가진 <div>가 생성된다. 이 태그로 데이터 유무 판별하면된다.
                print(rankElements[1].find('div',{'class' : 'no_record'}))
                '''

                if rankElements[0].find('div',
                                        {'class': 'no_record'}) != None:  # 인덱스 0 : 경쟁전 fpp -> 정보가 있는지 없는지 유무를 판별한다.
                    embed = discord.Embed(title="Record not found", description="Rank TPP record not found.",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)

                    await message.channel.send("PUBG player " + playerNickname + "'s TPP Ranking information",
                                               embed=embed)
                else:
                    # Short of fpp Rank
                    fR = rankElements[0]
                    # Tier Information

                    # Get tier medal image
                    tierMedalImage = fR.find('div', {'class': 'grade-info'}).img['src']
                    # Get tier Information
                    tierInfo = fR.find('div', {'class': 'grade-info'}).img['alt']

                    # Rating Inforamtion
                    # RP Score
                    RPScore = fR.find('div', {'class': 'rating'}).find('span', {'class': 'caption'}).text

                    # Get top rate statistics

                    # 등수
                    topRatioRank = topRatio = fR.find('p', {'class': 'desc'}).find('span', {'class': 'rank'}).text
                    # 상위 %
                    topRatio = fR.find('p', {'class': 'desc'}).find('span', {'class': 'top'}).text

                    # Main : Stats all in here.

                    mainStatsLayout = fR.find('div', {'class': 'stats'})

                    # Stats Data Saved As List

                    statsList = mainStatsLayout.findAll('p', {'class': 'value'})  # [KDA,승률,Top10,평균딜량, 게임수, 평균등수]
                    statsRatingList = mainStatsLayout.findAll('span', {'class': 'top'})  # [KDA, 승률,Top10 평균딜량, 게임수]

                    for r in range(0, len(statsList)):
                        # \n으로 큰 여백이 있어 split 처리
                        statsList[r] = statsList[r].text.strip().split('\n')[0]
                        statsRatingList[r] = statsRatingList[r].text
                    # 평균등수는 stats Rating을 표시하지 않는다.
                    statsRatingList = statsRatingList[0:5]

                    embed = discord.Embed(title="배그 전적", description="",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    embed.add_field(name="Real Time Accessors and Server Status",
                                    value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                          serverAccessorAndStatus[1].split(':')[-1], inline=False)
                    embed.add_field(name="Player located server", value=seasonInfo[2] + " Server", inline=False)
                    embed.add_field(name="Tier / Top Rate / Average Rank",
                                    value=tierInfo + " (" + RPScore + ") / " + topRatio + " / " + topRatioRank,
                                    inline=False)
                    embed.add_field(name="K/D", value=statsList[0] + "/" + statsRatingList[0], inline=True)
                    embed.add_field(name="승률", value=statsList[1] + "/" + statsRatingList[1], inline=True)
                    embed.add_field(name="Top 10 비율", value=statsList[2] + "/" + statsRatingList[2], inline=True)
                    embed.add_field(name="평균딜량", value=statsList[3] + "/" + statsRatingList[3], inline=True)
                    embed.add_field(name="게임수", value=statsList[4] + "판/" + statsRatingList[4], inline=True)
                    embed.add_field(name="평균등수", value=statsList[5], inline=True)
                    embed.set_thumbnail(url=f'https:{tierMedalImage}')

                    await message.channel.send("PUBG player " + playerNickname + "'s TPP Ranking information",
                                               embed=embed)


        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)
            print(e)
        except AttributeError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)
            print(e)

    if message.content.startswith("마고야경쟁전2"):  # FPP
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)

        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x8285FA)
                embed.add_field(name="Player nickname not entered",
                                value="To use command 마고야경쟁전(1 : TPP or 2 : FPP) : 마고야경쟁전 (Nickname)", inline=False)

                await message.channel.send("Error : Incorrect command usage ", embed=embed)
            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                # index 0: fpp 1 : tpp

                rankElements = bs.findAll('div', {'class': re.compile('squad ranked [A-Za-z0-9]')})

                '''
                -> 클래스 값을 가져와서 판별하는 것도 있지만 이 방법을 사용해 본다.
                -> 만약 기록이 존재 하지 않는 경우 class 가 no_record라는 값을 가진 <div>가 생성된다. 이 태그로 데이터 유무 판별하면된다.
                print(rankElements[1].find('div',{'class' : 'no_record'}))
                '''

                if rankElements[1].find('div',
                                        {'class': 'no_record'}) != None:  # 인덱스 0 : 경쟁전 fpp -> 정보가 있는지 없는지 유무를 판별한다a.
                    embed = discord.Embed(title="Record not found", description="Solo que record not found.",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)

                    await message.channel.send("PUBG player " + playerNickname + "'s FPP Ranking information",
                                               embed=embed)
                else:
                    # Short of fpp Rank
                    fR = rankElements[1]
                    # Tier Information

                    # Get tier medal image
                    tierMedalImage = fR.find('div', {'class': 'grade-info'}).img['src']
                    # Get tier Information
                    tierInfo = fR.find('div', {'class': 'grade-info'}).img['alt']

                    # Rating Inforamtion
                    # RP Score
                    RPScore = fR.find('div', {'class': 'rating'}).find('span', {'class': 'caption'}).text

                    # Get top rate statistics

                    # 등수
                    topRatioRank = topRatio = fR.find('p', {'class': 'desc'}).find('span', {'class': 'rank'}).text
                    # 상위 %
                    topRatio = fR.find('p', {'class': 'desc'}).find('span', {'class': 'top'}).text

                    # Main : Stats all in here.

                    mainStatsLayout = fR.find('div', {'class': 'stats'})

                    # Stats Data Saved As List

                    statsList = mainStatsLayout.findAll('p', {'class': 'value'})  # [KDA,승률,Top10,평균딜량, 게임수, 평균등수]
                    statsRatingList = mainStatsLayout.findAll('span', {'class': 'top'})  # [KDA, 승률,Top10 평균딜량, 게임수]

                    for r in range(0, len(statsList)):
                        # \n으로 큰 여백이 있어 split 처리
                        statsList[r] = statsList[r].text.strip().split('\n')[0]
                        statsRatingList[r] = statsRatingList[r].text
                    # 평균등수는 stats Rating을 표시하지 않는다.
                    statsRatingList = statsRatingList[0:5]

                    embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    embed.add_field(name="Real Time Accessors and Server Status",
                                    value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                          serverAccessorAndStatus[1].split(':')[-1], inline=False)
                    embed.add_field(name="Player located server", value=seasonInfo[2] + " Server", inline=False)
                    embed.add_field(name="Tier / Top Rate / Average Rank",
                                    value=tierInfo + " (" + RPScore + ") / " + topRatio + " / " + topRatioRank,
                                    inline=False)
                    embed.add_field(name="K/D", value=statsList[0] + "/" + statsRatingList[0], inline=True)
                    embed.add_field(name="승률", value=statsList[1] + "/" + statsRatingList[1], inline=True)
                    embed.add_field(name="Top 10 비율", value=statsList[2] + "/" + statsRatingList[2], inline=True)
                    embed.add_field(name="평균딜량", value=statsList[3] + "/" + statsRatingList[3], inline=True)
                    embed.add_field(name="게임수", value=statsList[4] + "판/" + statsRatingList[4], inline=True)
                    embed.add_field(name="평균등수", value=statsList[5], inline=True)
                    embed.set_thumbnail(url=f'https:{tierMedalImage}')

                    await message.channel.send("PUBG player " + playerNickname + "'s FPP Ranking information",
                                               embed=embed)


        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)
        except AttributeError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("마고야배그솔로1"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x8285FA)
                embed.add_field(name="Player nickname not entered",
                                value="To use command 마고야배그솔로 : 마고야배그솔로 (Nickname)", inline=False)

                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                soloQueInfo = bs.find('section', {'class': "solo modeItem"}).find('div', {'class': "mode-section tpp"})
                if soloQueInfo == None:
                    embed = discord.Embed(title="Record not found", description="Solo que record not found.",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    await message.channel.send("PUBG player " + playerNickname + "'s TPP solo que information",
                                               embed=embed)
                else:
                    # print(soloQueInfo)
                    # Get total playtime
                    soloQueTotalPlayTime = soloQueInfo.find('span', {'class': "time_played"}).text.strip()
                    # Get Win/Top10/Lose : [win,top10,lose]
                    soloQueGameWL = soloQueInfo.find('em').text.strip().split(' ')
                    # RankPoint
                    rankPoint = soloQueInfo.find('span', {'class': 'value'}).text
                    # Tier image url, tier
                    tierInfos = soloQueInfo.find('img', {
                        'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                    tierImage = "https:" + tierInfos['src']
                    print(tierImage)
                    tier = tierInfos['alt']

                    # Comprehensive info
                    comInfo = []
                    # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                    for ci in soloQueInfo.findAll('p', {'class': 'value'}):
                        comInfo.append(''.join(ci.text.split()))

                    embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    embed.add_field(name="Real Time Accessors and Server Status",
                                    value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                          serverAccessorAndStatus[1].split(':')[-1], inline=False)
                    embed.add_field(name="Player located server",
                                    value=seasonInfo[2] + " Server / Total playtime : " + soloQueTotalPlayTime,
                                    inline=False)
                    embed.add_field(name="Tier",
                                    value=tier + " (" + rankPoint + "p)", inline=False)
                    embed.add_field(name="K/D", value=comInfo[0], inline=True)
                    embed.add_field(name="승률", value=comInfo[1], inline=True)
                    embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                    embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                    embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                    embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                    embed.add_field(name="헤드샷 비율", value=comInfo[6], inline=True)
                    embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                    embed.add_field(name="평균생존시간", value=comInfo[8], inline=True)

                    await message.channel.send("PUBG player " + playerNickname + "'s TPP solo que information",
                                               embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)
        except AttributeError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("마고야배그듀오1"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x8285FA)
                embed.add_field(name="Player nickname not entered",
                                value="To use command 마고야배그스쿼드 : 마고야배그스쿼드 (Nickname)", inline=False)

                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                duoQueInfo = bs.find('section', {'class': "duo modeItem"}).find('div', {'class': "mode-section tpp"})
                if duoQueInfo == None:
                    embed = discord.Embed(title="Record not found", description="Duo que record not found.",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    await message.channel.send("PUBG player " + playerNickname + "'s TPP duo que information",
                                               embed=embed)
                else:
                    # print(duoQueInfo)
                    # Get total playtime
                    duoQueTotalPlayTime = duoQueInfo.find('span', {'class': "time_played"}).text.strip()
                    # Get Win/Top10/Lose : [win,top10,lose]
                    duoQueGameWL = duoQueInfo.find('em').text.strip().split(' ')
                    # RankPoint
                    rankPoint = duoQueInfo.find('span', {'class': 'value'}).text
                    # Tier image url, tier
                    tierInfos = duoQueInfo.find('img', {
                        'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                    tierImage = "https:" + tierInfos['src']
                    tier = tierInfos['alt']

                    # Comprehensive info
                    comInfo = []
                    # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                    for ci in duoQueInfo.findAll('p', {'class': 'value'}):
                        comInfo.append(''.join(ci.text.split()))

                    embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    embed.add_field(name="Real Time Accessors and Server Status",
                                    value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                          serverAccessorAndStatus[1].split(':')[-1], inline=False)
                    embed.add_field(name="Player located server and total playtime",
                                    value=seasonInfo[2] + " Server / Total playtime : " + duoQueTotalPlayTime,
                                    inline=False)
                    embed.add_field(name="Tier(Rank Point)",
                                    value=tier + " (" + rankPoint + "p)", inline=False)
                    embed.add_field(name="K/D", value=comInfo[0], inline=True)
                    embed.add_field(name="승률", value=comInfo[1], inline=True)
                    embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                    embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                    embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                    embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                    embed.add_field(name="헤드샷 비율", value=comInfo[6], inline=True)
                    embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                    embed.add_field(name="평균생존시간", value=comInfo[8], inline=True)

                    await message.channel.send("PUBG player " + playerNickname + "'s TPP duo que information",
                                               embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)
        except AttributeError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("마고야배그스쿼드1"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x8285FA)
                embed.add_field(name="Player nickname not entered",
                                value="To use command 마고야배그솔로 : 마고야배그솔로 (Nickname)", inline=False)

                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                squadQueInfo = bs.find('section', {'class': "squad modeItem"}).find('div',
                                                                                    {'class': "mode-section tpp"})
                if squadQueInfo == None:
                    embed = discord.Embed(title="Record not found", description="Squad que record not found.",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    await message.channel.send("PUBG player " + playerNickname + "'s TPP squad que information",
                                               embed=embed)
                else:
                    # print(duoQueInfo)
                    # Get total playtime
                    squadQueTotalPlayTime = squadQueInfo.find('span', {'class': "time_played"}).text.strip()
                    # Get Win/Top10/Lose : [win,top10,lose]
                    squadQueGameWL = squadQueInfo.find('em').text.strip().split(' ')
                    # RankPoint
                    rankPoint = squadQueInfo.find('span', {'class': 'value'}).text
                    # Tier image url, tier
                    tierInfos = squadQueInfo.find('img', {
                        'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                    tierImage = "https:" + tierInfos['src']
                    tier = tierInfos['alt']

                    # Comprehensive info
                    comInfo = []
                    # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                    for ci in squadQueInfo.findAll('p', {'class': 'value'}):
                        comInfo.append(''.join(ci.text.split()))
                    embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    embed.add_field(name="Real Time Accessors and Server Status",
                                    value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                          serverAccessorAndStatus[1].split(':')[-1], inline=False)
                    embed.add_field(name="Player located server",
                                    value=seasonInfo[2] + " Server / Total playtime : " + squadQueTotalPlayTime,
                                    inline=False)
                    embed.add_field(name="Tier(Rank Point)",
                                    value=tier + " (" + rankPoint + "p)", inline=False)
                    embed.add_field(name="K/D", value=comInfo[0], inline=True)
                    embed.add_field(name="승률", value=comInfo[1], inline=True)
                    embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                    embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                    embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                    embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                    embed.add_field(name="헤드샷 비율", value=comInfo[6], inline=True)
                    embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                    embed.add_field(name="평균생존시간", value=comInfo[8], inline=True)

                    await message.channel.send("PUBG player " + playerNickname + "'s TPP squad que information",
                                               embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)
        except AttributeError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("마고야배그솔로2"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x8285FA)
                embed.add_field(name="Player nickname not entered",
                                value="To use command 마고야배그솔로 : 마고야배그솔로 (Nickname)", inline=False)

                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                soloQueInfo = bs.find('section', {'class': "solo modeItem"}).find('div', {'class': "mode-section fpp"})
                if soloQueInfo == None:
                    embed = discord.Embed(title="Record not found", description="Solo que record not found.",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    await message.channel.send("PUBG player " + playerNickname + "'s FPP solo que information",
                                               embed=embed)
                else:
                    # print(soloQueInfo)
                    # Get total playtime
                    soloQueTotalPlayTime = soloQueInfo.find('span', {'class': "time_played"}).text.strip()
                    # Get Win/Top10/Lose : [win,top10,lose]
                    soloQueGameWL = soloQueInfo.find('em').text.strip().split(' ')
                    # RankPoint
                    rankPoint = soloQueInfo.find('span', {'class': 'value'}).text
                    # Tier image url, tier
                    tierInfos = soloQueInfo.find('img', {
                        'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                    tierImage = "https:" + tierInfos['src']
                    print(tierImage)
                    tier = tierInfos['alt']

                    # Comprehensive info
                    comInfo = []
                    # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                    for ci in soloQueInfo.findAll('p', {'class': 'value'}):
                        comInfo.append(''.join(ci.text.split()))
                    embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    embed.add_field(name="Real Time Accessors and Server Status",
                                    value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                          serverAccessorAndStatus[1].split(':')[-1], inline=False)
                    embed.add_field(name="Player located server",
                                    value=seasonInfo[2] + " Server / Total playtime : " + soloQueTotalPlayTime,
                                    inline=False)
                    embed.add_field(name="Tier(Rank Point)",
                                    value=tier + " (" + rankPoint + "p)", inline=False)
                    embed.add_field(name="K/D", value=comInfo[0], inline=True)
                    embed.add_field(name="승률", value=comInfo[1], inline=True)
                    embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                    embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                    embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                    embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                    embed.add_field(name="헤드샷 비율", value=comInfo[6], inline=True)
                    embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                    embed.add_field(name="평균생존시간", value=comInfo[8], inline=True)

                    await message.channel.send("PUBG player " + playerNickname + "'s FPP solo que information",
                                               embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)
        except AttributeError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("마고야배그듀오2"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x8285FA)
                embed.add_field(name="Player nickname not entered",
                                value="To use command 마고야배그스쿼드 : 마고야배그스쿼드 (Nickname)", inline=False)

                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                duoQueInfo = bs.find('section', {'class': "duo modeItem"}).find('div', {'class': "mode-section fpp"})
                if duoQueInfo == None:
                    embed = discord.Embed(title="Record not found", description="Duo que record not found.",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    await message.channel.send("PUBG player " + playerNickname + "'s FPP duo que information",
                                               embed=embed)
                else:
                    # print(duoQueInfo)
                    # Get total playtime
                    duoQueTotalPlayTime = duoQueInfo.find('span', {'class': "time_played"}).text.strip()
                    # Get Win/Top10/Lose : [win,top10,lose]
                    duoQueGameWL = duoQueInfo.find('em').text.strip().split(' ')
                    # RankPoint
                    rankPoint = duoQueInfo.find('span', {'class': 'value'}).text
                    # Tier image url, tier
                    tierInfos = duoQueInfo.find('img', {
                        'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                    tierImage = "https:" + tierInfos['src']
                    tier = tierInfos['alt']

                    # Comprehensive info
                    comInfo = []
                    # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                    for ci in duoQueInfo.findAll('p', {'class': 'value'}):
                        comInfo.append(''.join(ci.text.split()))
                    embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    embed.add_field(name="Real Time Accessors and Server Status",
                                    value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                          serverAccessorAndStatus[1].split(':')[-1], inline=False)
                    embed.add_field(name="Player located server and total playtime",
                                    value=seasonInfo[2] + " Server / Total playtime : " + duoQueTotalPlayTime,
                                    inline=False)
                    embed.add_field(name="Tier(Rank Point)",
                                    value=tier + " (" + rankPoint + "p)", inline=False)
                    embed.add_field(name="K/D", value=comInfo[0], inline=True)
                    embed.add_field(name="승률", value=comInfo[1], inline=True)
                    embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                    embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                    embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                    embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                    embed.add_field(name="헤드샷 비율", value=comInfo[6], inline=True)
                    embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                    embed.add_field(name="평균생존시간", value=comInfo[8], inline=True)

                    await message.channel.send("PUBG player " + playerNickname + "'s FPP duo que information",
                                               embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)
        except AttributeError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)

    if message.content.startswith("마고야배그스쿼드2"):
        baseURL = "https://dak.gg/profile/"
        playerNickname = ''.join((message.content).split(' ')[1:])
        URL = baseURL + quote(playerNickname)
        try:
            html = urlopen(URL)
            bs = BeautifulSoup(html, 'html.parser')
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x8285FA)
                embed.add_field(name="Player nickname not entered",
                                value="To use command 마고야배그솔로 : 마고야배그솔로 (Nickname)", inline=False)

                await message.channel.send("Error : Incorrect command usage ", embed=embed)

            else:
                accessors = bs.findAll('a', {'href': re.compile('\/statistics\/[A-Za-z]')})

                # Season Information : ['PUBG',(season info),(Server),'overview']
                seasonInfo = []
                for si in bs.findAll('li', {'class': "active"}):
                    seasonInfo.append(si.text.strip())
                serverAccessorAndStatus = []
                # To prevent : Parsing Server Status, Make a result like Server:\nOnline. So I need to delete '\n'to get good result
                for a in accessors:
                    serverAccessorAndStatus.append(re.sub(pattern='[\n]', repl="", string=a.text.strip()))

                # Varaible serverAccessorAndStatus : [(accessors),(ServerStatus),(Don't needed value)]

                squadQueInfo = bs.find('section', {'class': "squad modeItem"}).find('div',
                                                                                    {'class': "mode-section fpp"})
                if squadQueInfo == None:
                    embed = discord.Embed(title="Record not found", description="Squad que record not found.",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    await message.channel.send("PUBG player " + playerNickname + "'s FPP squad que information",
                                               embed=embed)
                else:
                    # print(duoQueInfo)
                    # Get total playtime
                    squadQueTotalPlayTime = squadQueInfo.find('span', {'class': "time_played"}).text.strip()
                    # Get Win/Top10/Lose : [win,top10,lose]
                    squadQueGameWL = squadQueInfo.find('em').text.strip().split(' ')
                    # RankPoint
                    rankPoint = squadQueInfo.find('span', {'class': 'value'}).text
                    # Tier image url, tier
                    tierInfos = squadQueInfo.find('img', {
                        'src': re.compile('\/\/static\.dak\.gg\/images\/icons\/tier\/[A-Za-z0-9_.]')})
                    tierImage = "https:" + tierInfos['src']
                    tier = tierInfos['alt']

                    # Comprehensive info
                    comInfo = []
                    # [K/D,승률,Top10,평균딜량,게임수, 최다킬수,헤드샷,저격거리,생존,평균순위]
                    for ci in squadQueInfo.findAll('p', {'class': 'value'}):
                        comInfo.append(''.join(ci.text.split()))
                    embed = discord.Embed(title="Player Unkonw Battle Ground player search from dak.gg", description="",
                                          color=0x8285FA)
                    embed.add_field(name="Player search from dak.gg", value=URL, inline=False)
                    embed.add_field(name="Real Time Accessors and Server Status",
                                    value="Accessors : " + serverAccessorAndStatus[0] + " | " "Server Status : " +
                                          serverAccessorAndStatus[1].split(':')[-1], inline=False)
                    embed.add_field(name="Player located server",
                                    value=seasonInfo[2] + " Server / Total playtime : " + squadQueTotalPlayTime,
                                    inline=False)
                    embed.add_field(name="Tier(Rank Point)",
                                    value=tier + " (" + rankPoint + "p)", inline=False)
                    embed.add_field(name="K/D", value=comInfo[0], inline=True)
                    embed.add_field(name="승률", value=comInfo[1], inline=True)
                    embed.add_field(name="Top 10 비율", value=comInfo[2], inline=True)
                    embed.add_field(name="평균딜량", value=comInfo[3], inline=True)
                    embed.add_field(name="게임수", value=comInfo[4] + "판", inline=True)
                    embed.add_field(name="최다킬수", value=comInfo[5] + "킬", inline=True)
                    embed.add_field(name="헤드샷 비율", value=comInfo[6], inline=True)
                    embed.add_field(name="저격거리", value=comInfo[7], inline=True)
                    embed.add_field(name="평균생존시간", value=comInfo[8], inline=True)

                    await message.channel.send("PUBG player " + playerNickname + "'s FPP squad que information",
                                               embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)
        except AttributeError as e:
            embed = discord.Embed(title="Not existing plyer",
                                  description="Can't find player " + playerNickname + "'s information.\nPlease check player's nickname again",
                                  color=0x8285FA)
            await message.channel.send("Error : Not existing player", embed=embed)



    if message.content.startswith("마고야한영번역"):

        baseurl = "https://openapi.naver.com/v1/papago/n2mt"

        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word

                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)
                print(combineword)

                dataParmas = "source=ko&target=en&text=" + combineword

                request = Request(baseurl)

                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()

                    api_callResult = response_body.decode('utf-8')

                    api_callResult = json.loads(api_callResult)

                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> English", description="", color=0x8285FA)
                    embed.add_field(name="한국어", value=savedCombineword, inline=False)
                    embed.add_field(name="영어", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")

                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("마고야영한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"

        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word

                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                dataParmas = "source=en&target=ko&text=" + combineword

                request = Request(baseurl)

                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()

                    api_callResult = response_body.decode('utf-8')


                    api_callResult = json.loads(api_callResult)

                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | English -> Korean", description="", color=0x8285FA)
                    embed.add_field(name="영어", value=savedCombineword, inline=False)
                    embed.add_field(name="한국어", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")

                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("마고야한일번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"

        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word

                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                dataParmas = "source=ko&target=ja&text=" + combineword

                request = Request(baseurl)

                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()

                    api_callResult = response_body.decode('utf-8')


                    api_callResult = json.loads(api_callResult)

                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> Japanese", description="", color=0x8285FA)
                    embed.add_field(name="한국어", value=savedCombineword, inline=False)
                    embed.add_field(name="일본어", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")

                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("마고야일한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"

        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word

                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                dataParmas = "source=ja&target=ko&text=" + combineword

                request = Request(baseurl)

                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()

                    api_callResult = response_body.decode('utf-8')


                    api_callResult = json.loads(api_callResult)

                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Japanese -> Korean", description="", color=0x8285FA)
                    embed.add_field(name="일본어", value=savedCombineword, inline=False)
                    embed.add_field(name="한국어", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")

                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("마고야한중번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"

        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                dataParmas = "source=ko&target=zh-CN&text=" + combineword

                request = Request(baseurl)

                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()

                    api_callResult = response_body.decode('utf-8')

                    api_callResult = json.loads(api_callResult)

                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Korean -> Chinese(Simplified Chinese)", description="",
                                          color=0x5CD1E5)
                    embed.add_field(name="한국어", value=savedCombineword, inline=False)
                    embed.add_field(name="중국어", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")

                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("마고야중한번역"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"

        trsText = message.content.split(" ")
        try:
            if len(trsText) == 1:
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word

                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                dataParmas = "source=zh-CN&target=ko&text=" + combineword


                request = Request(baseurl)

                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200):
                    response_body = response.read()

                    api_callResult = response_body.decode('utf-8')

                    api_callResult = json.loads(api_callResult)

                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate | Chinese -> Korean", description="", color=0x8285FA)
                    embed.add_field(name="중국어", value=savedCombineword, inline=False)
                    embed.add_field(name="한국어", value=translatedText, inline=False)
                    embed.set_thumbnail(url="https://papago.naver.com/static/img/papago_og.png")

                    await message.channel.send("Translate complete", embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)
        except HTTPError as e:
            await message.channel.send("Translate Failed. HTTPError Occured.")

    if message.content.startswith("마고야 코로나"):
        # 보건복지부 코로나 바이러스 정보사이트"
        covidSite = "http://ncov.mohw.go.kr/index.jsp"
        covidNotice = "http://ncov.mohw.go.kr"
        html = urlopen(covidSite)
        bs = BeautifulSoup(html, 'html.parser')
        latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[0][1:].split('.')
        statisticalNumbers = bs.findAll('span', {'class': 'num'})
        beforedayNumbers = bs.findAll('span', {'class': 'before'})

        # 주요 브리핑 및 뉴스링크
        briefTasks = []
        mainbrief = bs.findAll('a', {'href': re.compile('\/tcmBoardView\.do\?contSeq=[0-9]*')})
        for brf in mainbrief:
            container = []
            container.append(brf.text)
            container.append(covidNotice + brf['href'])
            briefTasks.append(container)
        print(briefTasks)

        # 통계수치
        statNum = []
        # 전일대비 수치
        beforeNum = []
        for num in range(7):
            statNum.append(statisticalNumbers[num].text)
        for num in range(4):
            beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

        totalPeopletoInt = statNum[0].split(')')[-1].split(',')
        tpInt = ''.join(totalPeopletoInt)
        lethatRate = round((int(statNum[3]) / int(tpInt)) * 100, 2)
        embed = discord.Embed(title="대한민국 코로나 현황", description="", color=0x8285FA)
        embed.add_field(name="자료 출처",
                        value="http://ncov.mohw.go.kr/index.jsp", inline=False)
        embed.add_field(name="자료 업데이트 시간",
                        value="해당 자료는 " + latestupdateTime[0] + "월 " + latestupdateTime[1] + "일 " +
                              latestupdateTime[2] + " 자료입니다.", inline=False)
        embed.add_field(name="확진환자(누적)", value=statNum[0].split(')')[-1] + "(" + beforeNum[0] + ")",
                        inline=True)
        embed.add_field(name="완치환자(격리해제)", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
        embed.add_field(name="치료중(격리 중)", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
        embed.add_field(name="사망", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
        embed.add_field(name="누적확진률", value=statNum[6], inline=True)
        embed.add_field(name="치사율", value=str(lethatRate) + " %", inline=True)
        embed.add_field(name="- 최신 브리핑 1 : " + briefTasks[0][0], value="링크 : " + briefTasks[0][1],
                        inline=False)
        embed.add_field(name="- 최신 브리핑 2 : " + briefTasks[1][0], value="링크 : " + briefTasks[1][1],
                        inline=False)
        embed.set_thumbnail(
            url="https://wikis.krsocsci.org/images/7/79/%EB%8C%80%ED%95%9C%EC%99%95%EA%B5%AD_%ED%83%9C%EA%B7%B9%EA%B8%B0.jpg")

        await message.channel.send("Covid-19 Virus Korea Status", embed=embed)

    if message.content.startswith('마고야메이플'):

        # Maplestroy base link
        mapleLink = "https://maplestory.nexon.com"
        # Maplestory character search base link
        mapleCharacterSearch = "https://maplestory.nexon.com/Ranking/World/Total?c="
        mapleUnionLevelSearch = "https://maplestory.nexon.com/Ranking/Union?c="

        playerNickname = ''.join((message.content).split(' ')[1:])
        html = urlopen(mapleCharacterSearch + quote(playerNickname))  # Use quote() to prevent ascii error
        bs = BeautifulSoup(html, 'html.parser')

        html2 = urlopen(mapleUnionLevelSearch + quote(playerNickname))
        bs2 = BeautifulSoup(html2, 'html.parser')

        if len(message.content.split(" ")) == 1:
            embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x8285FA)
            embed.add_field(name="Player nickname not entered",
                            value="To use command 마고야 메이플 : 마고야 메이플 (Nickname)", inline=False)

            await message.channel.send("Error : Incorrect command usage ", embed=embed)

        elif bs.find('tr', {'class': 'search_com_chk'}) == None:
            embed = discord.Embed(title="Nickname not exist", description="", color=0x8285FA)
            embed.add_field(name="해당 닉네임의 플레이어가 존재하지 않습니다.", value="플레이어 이름을 확인해주세요", inline=False)

            await message.channel.send("Error : Non existing Summoner ", embed=embed)

        else:
            # Get to the character info page
            characterRankingLink = bs.find('tr', {'class': 'search_com_chk'}).find('a', {
                'href': re.compile('\/Common\/Character\/Detail\/[A-Za-z0-9%?=]*')})['href']
            # Parse Union Level
            characterUnionRanking = bs2.find('tr', {'class': 'search_com_chk'})
            if characterUnionRanking == None:
                pass
            else:
                characterUnionRanking = characterUnionRanking.findAll('td')[2].text
            html = urlopen(mapleLink + characterRankingLink)
            bs = BeautifulSoup(html, 'html.parser')

            # Find Ranking page and parse page
            personalRankingPageURL = bs.find('a', {
                'href': re.compile('\/Common\/Character\/Detail\/[A-Za-z0-9%?=]*\/Ranking\?p\=[A-Za-z0-9%?=]*')})[
                'href']
            html = urlopen(mapleLink + personalRankingPageURL)
            bs = BeautifulSoup(html, 'html.parser')
            # Popularity

            popularityInfo = bs.find('span', {'class': 'pop_data'}).text.strip()
            ''' Can't Embed Character's image. Gonna fix it after patch note
            #Character image
            getCharacterImage = bs.find('img',{'src': re.compile('https\:\/\/avatar\.maplestory\.nexon\.com\/Character\/[A-Za-z0-9%?=/]*')})['src']
            '''
            infoList = []

            RankingInformation = bs.findAll(
                'dd')
            for inf in RankingInformation:
                infoList.append(inf.text)
            embed = discord.Embed(title="[" + playerNickname + "]의 정보",
                                  description=infoList[0] + " | " + infoList[1] + " | " + "서버 : " + infoList[2],
                                  color=0x8285FA)
            embed.add_field(name="종합 랭킹", value=infoList[4], inline=True)
            embed.add_field(name="게임 랭킹", value=infoList[6], inline=True)
            embed.add_field(name="직업 랭킹", value=infoList[8], inline=True)
            embed.add_field(name="인기도 랭킹", value=infoList[10] + "( " + popularityInfo + " )", inline=True)
            if characterUnionRanking == None:
                embed.add_field(name="총합 레벨", value=infoList[12], inline=True)
            else:
                embed.add_field(name="총합 레벨", value=infoList[12] + "( LV." + characterUnionRanking + " )",
                                inline=True)
            embed.add_field(name="업적 랭킹", value=infoList[14], inline=True)
            embed.set_thumbnail(url='https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png')

            await message.channel.send("Player " + playerNickname + "'s information search", embed=embed)






    if message.content.startswith("마고야 음식추천"):
        food = "삼겹살 곱창 스테이크 초밥 회 후라이드치킨 육회 대게찜 떡순튀 소갈비" \
               " 간장게장 랍스터버터구이 김치찌게 감자탕 양념치킨 라면 부대찌개 보쌈" \
               " 닭발 샤브샤브 닭갈비 햄버거 차돌박이 된장찌개 닭강정 김볶 피자 수육 " \
               "국밥 양념게장 찜닭 간장치킨 조개구기 닭도리탕 족발 탕수육 해물찜 양갈비" \
               " 물냉면 산낙지 크림파스타 닭꼬치 짜장면 불족발 양꼬치 설렁탕 갈비탕 " \
               "대하소금구이 훈제치킨 짬뽕 버팔로윙 떡국 타코야키 물회 돈까스 라멘 우동" \
               " 쭈꾸미볶음 바지락칼국수 훠궈 순두부찌개 제육볶음 잔치국수 깐쇼새우" \
               " 육개장 돼지껍데기 토마토스파게티 카레돈까스덮밥 오리주물럭 누룽지백숙" \
               " 비빔밥 수제비 로제파스타 소고기무국 삼계탕 해신탕 쌀국수 오일파스타 " \
               "낙지볶음 김밥 비빔냉면 함밥스테이크 매운탕 소떡소떡 알밥 토스트 선지해장국" \
               " 꼬막무침 대구내장탕 불고기 참치마요덮밥 카레 꿔바로우 메밀국수 샌드위치" \
               " 보리굴비 깐풍기 두부김치 청국장 치즈퐁듀 찐만두 쫄면 비빔국수 오므라이스" \
               " 문어숙회 묵사발 군만두 어묵 오코노미야끼 마파두부덮밥 물만두 중식볶음밥 " \
               "고등어조림 모듬전 타코 골뱅이무침 해물누룽지탕 추어탕 닭똥집 버섯전골 " \
               "콩국수 분짜 오징어볶음 과메기 잡채밥 소세지 콩나물밥"
        foodchoice = food.split(" ")
        foodnumber = random.randint(2,len(foodchoice))
        foodresult = foodchoice[foodnumber]
        await message.channel.send(foodresult + " 처머겅")
    if message.content.startswith("마고야 1부터10"):
        for x in range(10):
            await message.channel.send(x + 1)
    if message.content.startswith("마고야 계산"):
        global calcResult
        if message.content[7:].startswith("더하기"):
            calcResult = int(message.content[11:12]) + int(message.content[13:14])
            await message.channel.send("Result : " + str(calcResult))
        if message.content[7:].startswith("빼기"):
            calcResult = int(message.content[10:11]) - int(message.content[12:13])
            await message.channel.send("Result : " + str(calcResult))
        if message.content[7:].startswith("곱하기"):
            calcResult = int(message.content[11:12]) * int(message.content[13:14])
            await message.channel.send("Result : " + str(calcResult))
        if message.content[7:].startswith("나누기"):
            try:
                calcResult = int(message.content[11:12]) / int(message.content[13:14])
                await message.channel.send("Result : " + str(calcResult))
            except ZeroDivisionError:
                await message.channel.send("You can't divide with 0.")

@client.event
async def echo(ctx,*,content: str):
    await ctx.send(content)


@client.event
async def on_message_delete(message):
    await message.channel.send("메세지 삭제 감지(" + str(message.author) + "): " + message.content)
    return

@client.event
async def on_message_edit(before, after):
	await before.channel.send("메시지 수정 감지 (" + before.content + ") -> (" + after.content + ")")
	return

@client.event
async def on_reaction_add(reaction, user):
    await reaction.channel.send(reaction.content + user)
    return

@client.event
async def on_reaction_remove(reaction, user):
    await reaction.channel.send(reaction.content + user)
    return

@client.event
async def on_member_join(member):
	await member.guild.get_channel(743710662550880317).send(member.mention + "님이 새롭게 접속했습니다. 환영해주세요!")
	return

@client.event
async def on_member_remove(member):
    await member.guild.get_channel(743710662550880317).send(member.mention + "님이 서버를 나가셨어요.")















client.run(os.environ['token'])