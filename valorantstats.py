from discord.colour import Colour
import requests
from bs4 import BeautifulSoup
import discord

def valstats(ctx):
    msg = ctx.message.content.split('!stats ')
    x = msg[1].split("#")
    embed = None
    URL = "https://tracker.gg/valorant/profile/riot/"+x[0]+"%23"+x[1]+"/overview?playlist=competitive"
    page = requests.get(URL)
    embed=discord.Embed(title='Valorant Stats for ' + msg[1])

    soup = BeautifulSoup(page.content, "html.parser")
    err = soup.find('div',class_='content content--error')
    if (err != None):
        code = err.find('h1')
        if (code.text == '404'):
            return discord.Embed(title='Error 404: Player not found on Tracker.gg',description='Please make sure your Riot ID is linked to TRN. https://thetrackernetwork.com/manage/social')
        
    colors = [discord.Colour.dark_grey(),discord.Colour(9127187), discord.Colour.light_gray(), discord.Colour.gold(),discord.Colour.teal(),discord.Colour.purple(),0xbf374f,0xFFFFFE]
    color = 0

    #RANK
    rank = soup.find_all('span', class_='valorant-highlighted-stat__value')[0].text
    if (rank[-1] == 'R'):
        embed.add_field(name='Rank', value='Immortal '+rank, inline=False)
        color = colors[-2]
    else:
        embed.add_field(name='Rank', value=rank, inline=False)
        if rank[0] == 'I':
            color = colors[0]
        elif rank[0] == 'B':
            color = colors[1]
        elif rank[0] == 'S':
            color = colors[2]
        elif rank[0] == 'G':
            color = colors[3]
        elif rank[0] == 'P':
            color = colors[4]
        elif rank[0] == 'D':
            color = colors[5]
        print(color)
    embed.color = color

    giantstats = ['Damage/Round','K/D Ratio','Headshot%','Win %']
    gstats = soup.find_all('div', class_='giant-stats')

    agents = soup.find_all('div',class_='top-agents area-top-agents')

    #KAD
    kad = soup.find_all('span', class_='valorant-highlighted-stat__value')[1].text
    if (rank[-1] == 'R'):
        embed.add_field(name='Position', value=kad, inline=False)
    else:
        embed.add_field(name='KAD', value=kad, inline=False)

    stats = soup.find_all('div', class_='main')
    list = ['Wins','Kills','Headshots','Deaths','Assists','Score/Round','Kills/Round','First Bloods','Aces','Clutches','Flawless','Most Kills (Match)']
    img = soup.find('div',class_='valorant-highlighted-content__stats')
    img = img.find('img')
    print(img['src'])
    
    for x in gstats:
        z = x.find_all('span',class_='value')
    
    cnt = 0
    for i in z:
        embed.add_field(name=giantstats[cnt], value=str(i.text), inline=True)
        cnt+=1
    
    topagent = ''
    for i in agents:
        topagent = i.find('span',class_='agent__name').text
    
    agenturl = 'https://valorant-api.com/v1/agents'
    agentjson = requests.get(agenturl).json()

    agentpicture = ''
    for i in agentjson['data']:
        if (i['displayName'] == topagent):
            agentpicture = i["displayIcon"]

    embed.set_thumbnail(url=img['src'])
    embed.set_image(url=agentpicture)

    for y in stats:
        z = y.find_all('span',class_='value')
        cnt = 0
        for i in z:
            embed.add_field(name=list[cnt], value=str(i.text), inline=True)
            cnt+=1
    return embed