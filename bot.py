import discord
from discord.ext import commands
import valorantstats
import secretvars

ss = secretvars.secretvars()
TOKEN = ss.tokenid
GUILD = ss.guild
client = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    game = discord.Game("!stats {username#tag}")
    await bot.change_presence(activity=game)
    for guild in bot.guilds:
        print(f'{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})\n')
        if guild.name == GUILD:
            break

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.command(name='stats')
async def stat(ctx):
    await ctx.send(embed=valorantstats.valstats(ctx))

@bot.command(name='info')
async def info(ctx):
    await ctx.send(embed=discord.Embed(title="VALWATCH", description="A Discord bot that displays your Valorant stats.\n\nInvite this bot to your server or report any bugs using this link: https://github.com/shaheriar/VALWATCH", color=discord.Colour.red()))

bot.run(TOKEN)
