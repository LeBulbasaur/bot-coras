import discord
from discord import guild
from discord.ext import commands
from riotwatcher import LolWatcher
from Champions import getChampionName
import math
import asyncio
import youtube_dl
import os

client = commands.Bot(command_prefix=".")
TOKEN = "( ͡° ͜ʖ ͡°)"
KEY = "( ͡° ͜ʖ ͡°)"


watcher = LolWatcher(KEY)

server = "eun1"


# get user data


def getStats(summonerName):
    try:
        summoner = watcher.summoner.by_name(server, summonerName)
        stats = watcher.league.by_summoner(server, summoner["id"])
        return stats
    except:
        return "Gracz nie istnieje!"


# get favorite champion


def getChampion(id):
    champions = watcher.champion_mastery.by_summoner(server, id)
    return champions[0]


# get solo ranked data


def getSolo(data):
    for mode in data:
        if mode["queueType"] == "RANKED_SOLO_5x5":
            return mode


# choose rank graphic


def getRankImg(rank):
    if rank == "IRON":
        return "https://static.wikia.nocookie.net/leagueoflegends/images/0/03/Season_2019_-_Iron_1.png/revision/latest/scale-to-width-down/112?cb=20181229234926"
    elif rank == "BRONZE":
        return "https://static.wikia.nocookie.net/leagueoflegends/images/f/f4/Season_2019_-_Bronze_1.png/revision/latest/scale-to-width-down/112?cb=20181229234910"
    elif rank == "SILVER":
        return "https://static.wikia.nocookie.net/leagueoflegends/images/7/70/Season_2019_-_Silver_1.png/revision/latest/scale-to-width-down/112?cb=20181229234936"
    elif rank == "GOLD":
        return "https://static.wikia.nocookie.net/leagueoflegends/images/9/96/Season_2019_-_Gold_1.png/revision/latest/scale-to-width-down/112?cb=20181229234920"
    elif rank == "PLATINUM":
        return "https://static.wikia.nocookie.net/leagueoflegends/images/7/74/Season_2019_-_Platinum_1.png/revision/latest/scale-to-width-down/112?cb=20181229234932"
    elif rank == "DIAMOND":
        return "https://static.wikia.nocookie.net/leagueoflegends/images/9/91/Season_2019_-_Diamond_1.png/revision/latest/scale-to-width-down/112?cb=20181229234917"
    elif rank == "MASTER":
        return "https://static.wikia.nocookie.net/leagueoflegends/images/1/11/Season_2019_-_Master_1.png/revision/latest/scale-to-width-down/112?cb=20181229234929"
    elif rank == "GRANDMASTER":
        return "https://static.wikia.nocookie.net/leagueoflegends/images/7/76/Season_2019_-_Grandmaster_1.png/revision/latest/scale-to-width-down/112?cb=20181229234923"
    elif rank == "CHALLENGER":
        return "https://static.wikia.nocookie.net/leagueoflegends/images/5/5f/Season_2019_-_Challenger_1.png/revision/latest/scale-to-width-down/112?cb=20181229234913"


# bot wake up


@client.event
async def on_ready():
    print("kontrola lotu")


# clear messages


@client.command()
async def clear(ctx, num=None):
    if num:
        amount = int(num) + 1
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(
            colour=0xE3D58D
        )
        embed.set_image(
            url="https://animesher.com/orig/1/109/1096/10967/animesher.com_studio-ghibli-from-up-on-poppy-hill-1096756.gif")
        await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send("Brakuje liczby wiadomości do usunięcia!")


# display player info


@client.command()
async def stats(ctx, *nick):
    fullName = ""
    for word in nick:
        fullName = f"{fullName} {word}"
    if nick:
        try:
            statsSolo = getSolo(getStats(fullName))
        except:
            statsSolo = getSolo(getStats("6xSpace"))

        imgUrl = "https://static.wikia.nocookie.net/leagueoflegends/images/f/f7/Corki.Corki_na_Sankach.sk%C3%B3rka.jpg/revision/latest/scale-to-width-down/694?cb=20170221214001&path-prefix=pl"

        mostPlayedChampion = getChampion(statsSolo["summonerId"])
        championName = ""

        if getChampionName(mostPlayedChampion['championId']):
            championName = getChampionName(mostPlayedChampion['championId'])
            imgUrl = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{championName}_0.jpg"
        else:
            championName = "N/A"

        rankSolo = f"{statsSolo['tier']} {statsSolo['rank']}"

        lpSolo = statsSolo['leaguePoints']
        ratioValue = statsSolo['wins'] / \
            (statsSolo['wins'] + statsSolo['losses']) * 10000

        ratioSolo = f"{math.floor(ratioValue) / 100}%"

        rankImg = getRankImg(statsSolo['tier'])

        embed = discord.Embed(
            title=f"Gracz:",
            description=f"{fullName} 😼",
            colour=0xC66390
        )
        embed.set_author(name="stats by Coras",
                         icon_url="https://www.mobafire.com/images/avatars/corki-ice-toboggan.png")
        embed.set_thumbnail(
            url=rankImg)
        embed.add_field(name="Ranga Solo/Duo",
                        value=f"{rankSolo}", inline=True)
        embed.add_field(name="LP", value=f"{lpSolo}", inline=True)
        embed.add_field(name="Win rate", value=f"{ratioSolo}", inline=False)
        embed.add_field(name="Najwięcej zagrane",
                        value=f"{championName}", inline=False)
        embed.set_image(url=imgUrl)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Brakuje nicku!")


@client.command()
async def kontrola(ctx):
    if ctx.voice_client == None:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("./music/song.mp3"))
        await asyncio.sleep(4)
        await ctx.guild.voice_client.disconnect()

    else:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing() or voice.is_paused():
            await ctx.send("Widzisz mnie?")
        else:
            voice.play(discord.FFmpegPCMAudio("./music/kontrola.mp3"))
            await asyncio.sleep(4)
            await ctx.guild.voice_client.disconnect()


@client.command()
async def nightcore(ctx):
    if ctx.voice_client == None:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("./music/nightcore2019.mp3"))
    else:
        await ctx.send("Widzisz mnie?")


@client.command()
async def funny(ctx):
    if ctx.voice_client == None:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("./music/funny.mp3"))
    else:
        await ctx.send("Widzisz mnie?")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command()
async def spaduwa(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("mam robote")
    else:
        await ctx.send("Tak nie można!")


client.run(TOKEN)
