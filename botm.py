import discord 
from discord.utils import get 
import youtube_dl
from discord.ext import commands
import os

TOKEN="NzU2NDc5MDI0OTY4MjM3MTM1.X2Sb_g.TLcahZ9d2--tbkCh5eG470EWOKM"

bot=commands.Bot(command_prefix='--')
players={}

@bot.event
async def on_ready():
    print("Logged in as:-",bot.user.name,"\n") 

#----------make an if statement only execute when the user is in voice channel or print message 1st join voice channel------------#

@bot.command(pass_context=True,aliases=['j','joi'])
async def join(ctx):
    global voice
    channel=ctx.message.author.voice.channel
    voice=get(bot.voice_clients,guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice=await channel.connect()
    await voice.disconnect()

    if voice and voice.is_connected():
         await voice.move_to(channel)
    else:
        voice=await channel.connect()
        print(f"The bot has connected  to {channel}\n")
    
    await ctx.send(f"Bot joined {channel}")

@bot.command(pass_context=True,aliases=['l','lea'])
async def leave(ctx):
    channel=ctx.message.author.voice.channel
    voice=get(bot.voice_clients,guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Bot has left{channel}")
        await ctx.send(f"Left the {channel}")
    else:
        await ctx.send(f"I have  already left the channel")

@bot.command(pass_context=True)
async def play(ctx,url: str):
    song_there=os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Song has been Removed")
    except PermissionError:
        await ctx.send("ERROR: music  playing")
        return

    await ctx.send("Getting things ready")

    voice=get(bot.voice_clients,guild=ctx.guild)

    ydl_opts={
        'format':'bestaudio/best',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("downloading \n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name=file 
            os.rename(file,"song.mp3")
            print(f"Renamed file :{name}\n")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after= lambda e: print(f"{name} has finished playing"))
    voice.source=discord.PCMVolumeTransformer(voice.source)
    voice.source.volume=0.8 

    nname=url.rsplit("-", 2)
    await ctx.send(f"Playing :{nname[0]}")

@bot.command(pass_context=True, alianes=['pa', 'pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_playing():
        voice.pause()
        print("music paused")
        await ctx.send("Music paused")
    else:
        print("Song is not playing")
        await ctx.send("Song is not playing [Failed Pause]")


@bot.command(pass_context=True, alianes=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        voice.resume()
        print("Song is resumed")
        await ctx.send("Song resumed")
    else:
        print("Song is not paused")
        await ctx.send("Song is not paused [Resume Failed]")


@bot.command(pass_context=True, alianes=['s', 'sto'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and (voice.is_playing() or voice.is_paused()):
        voice.stop()
        print("music stoped")
        await ctx.send("Music stoped")
    else:
        print("Song is not playing")
        await ctx.send("Song is not playing [Stop Failed]")


bot.run(TOKEN)